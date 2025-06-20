import requests
import os
import json

token = input('Account token > ')

headers = {
    'Authorization': token,
}

backup_dir = 'gif_backup'
os.makedirs(backup_dir, exist_ok=True)

def get_favorites():
    r = requests.get('https://discord.com/api/v9/users/@me/gifs/favorites', headers=headers)
    return r.json().get('results', [])

def backup_gifs(gifs):
    with open('gifs_backup.json', 'w') as f:
        json.dump(gifs, f, indent=2)
      
    for gif in gifs:
        url = gif.get('src')
        if url:
            try:
                data = requests.get(url).content
                name = gif.get('id') or gif.get('src').split('/')[-1].split('?')[0]
                with open(os.path.join(backup_dir, name), 'wb') as f:
                    f.write(data)
            except:
                pass

def check_gif(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        return r.status_code == 200
    except:
        return False

def remove_favorite(gif_id):
    data = {'ids': [gif_id]}
    requests.post('https://discord.com/api/v9/users/@me/gifs/favorites/delete', headers=headers, json=data)

def main():
    gifs = get_favorites()
    backup_gifs(gifs)
    for gif in gifs:
        gif_id = gif.get('id')
        src = gif.get('src')
        if not check_gif(src):
            remove_favorite(gif_id)

main()
