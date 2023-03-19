import asyncio
import subprocess
import json
from config import config
import aiohttp
import re


async def completion(prompt: str) -> str:
    output: str = ''
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.openai_api_key}',
    }
    endpoint = 'https://api.openai.com/v1/engines/text-davinci-003/completions'
    params = {
        "prompt": prompt,
        "max_tokens": 600,
        "temperature": 0.8,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.6,
        "best_of": 1,
        "logprobs": 0,
        "stream": True
    }
    header_args = []
    for header in headers:
        header_args.append('-H')
        header_args.append(f'{header}: {headers[header]}')
    args = ['curl', '-X', 'POST', '-d', json.dumps(params), endpoint]
    args.extend(header_args)
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line_str: str = line.decode('utf-8')
        # print(line_str)
        if line_str.startswith('data:'):
            if '[DONE]' not in line_str:
                try:
                    data = json.loads(line_str[6:], strict=False)
                    token = data['choices'][0]['text']
                    print(token, end='')
                    output += token
                except Exception as e:
                    print(line_str[6:], end='')
    return output


def append_prompt(prompt: str, appended_prompt: str) -> str:
    _appended_prompt = f'\n\n{appended_prompt}\n'
    print(_appended_prompt)
    return prompt + _appended_prompt


def append_user_message(prompt: str, message: str) -> str:
    appended_prompt = f'[user](#message)\n{message}'
    return append_prompt(prompt, appended_prompt)


def append_system_search_result(prompt: str, search_result: str) -> str:
    appended_prompt = f'[system](#search_result)\n{search_result}'
    return append_prompt(prompt, appended_prompt)


def check_if_need_search(text: str) -> bool:
    if '(#online_search)' in text.strip():
        return True


async def perform_search(search_term: str) -> str:
    session = aiohttp.ClientSession()
    async with session.get(
            url='https://api.bing.microsoft.com/v7.0/search',
            params={
                'q': search_term,
                'count': config.search_results_count,
                'mkt': config.bing_language
            },
            headers={
                'Ocp-Apim-Subscription-Key': config.bing_api_key,
            }
    ) as resp:
        results: list[dict] = []
        response = await resp.json()
        for web_page in response['webPages']['value']:
            results.append({
                'title': web_page['name'],
                'snippet': web_page['snippet'],
            })
        await session.close()
        return json.dumps(results, ensure_ascii=False)


async def main():
    prompt = (
        '[system](#intro)'
        '\nYou are a smart AI assistant who can answer questions from users. You are helpful, polite, and friendly.'
        '\nYour responses should be informative, visual, logical and actionable.'
        '\nYour responses should also be positive, polite, interesting, entertaining and **engaging**.'
        '\nYour logic and reasoning should be rigorous and intelligent.'
        '\nTo respond to user, please reply:'
        '\n```'
        '\n[assistant](#response)   (new line)'
        '\nassistant message'
        '\n```'
        '\nBut your insider knowledge ends in 2021, and you **MUST** perform web searches when the user is seeking information (explicitly or implicitly), regardless of your internal knowledge or information.'
        '\nWhen you need to search, please reply:'
        '\n```'
        '\n[assistant](#online_search)   (new line)'
        '\nsearch term'
        '\n```'
        '\nand then **stop generating, wait for system to search** then generalize the result (ignore useless and irrelevant entries) and come up with an answer based on search results.'
    )
    print(prompt)

    appended_prompt = (
        '\n\n[system](#new_user)'
        '\nA new user has joined the conversation.'
        f'\nThis user is using {config.openai_language}.\n'
    )
    prompt += appended_prompt
    print(appended_prompt)

    # conversation starts ----

    try:
        while True:
            prompt = append_user_message(prompt, input('\n\nINPUT > '))

            output = await completion(prompt)
            if check_if_need_search(output):
                search_term = output.strip().split('\n')[1]
                print(f'\nSearching {search_term} ...')
                # Delete the last search result to prevent GPT from generating false search results by itself
                prompt = re.sub(r"\[system\]\(#search_result\)\n.+", "", prompt)
                search_result = await perform_search(search_term)
                prompt = append_system_search_result(prompt, search_result)
                prompt = append_prompt(prompt, '[assistant](#response)')
                output = await completion(prompt)
            prompt += (output + '\n')
    except KeyboardInterrupt:
        if config.save_chat_history:
            open(config.chat_history_filename, 'w').write(prompt)
        print('Down, miss you.')


asyncio.run(main())
