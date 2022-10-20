#!/usr/bin/env python3

import unittest
import requests.exceptions
from requests_html import HTMLSession
import csv
import os


def get_codewars_stats(username):
    """Scraps, and retrieves Codewars stats of given username."""
    session = HTMLSession()
    output = f'{username}\'s Codewars stats:\n'
    try:
        filepath = os.path.join(os.getcwd(), 'CodeWars')
        # Make Codewars directory if it does mot exist:
        if not os.path.isdir(filepath):
            os.mkdir(filepath)

        page = session.get(f'https://www.codewars.com/users/{username}', stream=True)
        stat_info = page.html.find('div.stat')
        important_values = [info.text for info in stat_info[:5] + stat_info[6:]]
        # Save user stats
        with open(os.path.join(filepath, f'{username}.txt'), 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file, delimiter='\n')
            writer.writerow(important_values)
        print('CodewarsStats have been successfully downloaded')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    try:
        # Get avatar/pic url
        img_url = page.html.find('figure.profile-pic', first=True).find('img', first=True).attrs['src']
        # make image_url requests, and save image:
        r = session.get(img_url, stream=True)
        with open(os.path.join(filepath, f'{username}.jpg'), 'wb') as fo:
            for chunk in r.iter_content(chunk_size=128):
                fo.write(chunk)
        print('CodewarsStats avatar has been successfully downloaded')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


class TestGetCodeWarsStats(unittest.TestCase):
    """Setup testing variables."""
    def setUp(self) -> None:
        # Feel free to use your username as a test sample instead:
        self.username_sample = 'seraph776'
        self.expected = get_codewars_stats(self.username_sample)


    def test_get_codewars_stats(self):
        """Tests get_codewars stats function."""
        self.assertEqual(get_codewars_stats(self.username_sample), self.expected)
        with self.assertRaises(Exception):
            get_codewars_stats('invalid_username')


if __name__ == '__main__':
    unittest.main()
