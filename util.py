import base64
import orjson
import os
import pathlib
import platform
import random
import re
import socket
import subprocess
import sys
import threading
import datetime
from typing import Optional
from selenium.webdriver.common.by import By

import requests
from typing import (
    Dict,
    Any
)

CONST_FROM_TOP_TO_BOTTOM = "from top to bottom"
CONST_FROM_BOTTOM_TO_TOP = "from bottom to top"
CONST_CENTER = "center"
CONST_RANDOM = "random"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def is_connectable(port: int, host: Optional[str] = "localhost") -> bool:
    """
    Check if a socket at the given host and port is connectable.

    Args:
        port (int): The port number to check.
        host (Optional[str], optional): The host to check. Defaults to "localhost".

    Returns:
        bool: True if the port is connectable, False otherwise.
    """
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (socket.error, ConnectionResetError):
        return False

def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from a given text.

    Args:
        text (str): The text to remove HTML tags from.

    Returns:
        str: The text with all HTML tags removed.
    """
    if text is None:
        return ""

    html_tag_pattern = re.compile('<.*?>')
    cleaned_text = re.sub(html_tag_pattern, '', text).strip()
    
    return cleaned_text

# common functions.
def find_between(input_string: str, start_string: str, end_string: str) -> str:
    """
    Find the string between two given strings.

    Args:
        input_string (str): The string to search in.
        start_string (str): The string to start searching from.
        end_string (str): The string to search until.

    Returns:
        str: The string between the two given strings.
    """
    try:
        start_index = input_string.index(start_string) + len(start_string)
        end_index = input_string.index(end_string, start_index)
        return input_string[start_index:end_index]
    except ValueError:
        return ""

def sx(input_string: str) -> str:
    """
    Perform XOR encryption/decryption on the given string with a fixed key.

    Args:
        input_string (str): The input string to be encrypted or decrypted.

    Returns:
        str: The resulting string after applying XOR operation with the key.
    """
    xor_key = 18
    return ''.join(chr(ord(char) ^ xor_key) for char in input_string)

def decryptMe(encrypted_string: str) -> str:
    decrypted_string = ""
    if encrypted_string:
        decrypted_string = sx(base64.b64decode(encrypted_string).decode("utf-8"))
    return decrypted_string

def encryptMe(plaintext: str) -> str:
    ciphertext = ""
    if plaintext:
        ciphertext = base64.b64encode(sx(plaintext).encode("utf-8")).decode("utf-8")
    return ciphertext

def is_arm() -> bool:
    return "-arm" in platform.platform()

import os
import sys

def get_app_root() -> str:
    """
    Determine the root directory of the application.

    If the application is frozen, the root directory is the parent directory
    of the executable. Otherwise, it is the current working directory.

    Returns:
        str: The application's root directory.
    """
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def format_config_keyword_for_json(config_keyword: str) -> str:
    """
    Format a string for use as a JSON keyword.

    If the string is not a JSON object or array, it is returned unchanged.
    If the string is a JSON object, the first item is extracted and returned as a string.
    If the string is a JSON array, the first item is returned as a string.

    Args:
        config_keyword (str): The input string to be formatted.

    Returns:
        str: The formatted string.
    """
    if not (config_keyword.startswith('"') and config_keyword.endswith('"')):
        config_keyword = f'"{config_keyword}"'
        
    try:
        json_data = orjson.loads(config_keyword)
        if isinstance(json_data, dict) and json_data:
            config_keyword = orjson.dumps(next(iter(json_data.values()))).decode('utf-8')
        elif isinstance(json_data, list) and json_data:
            config_keyword = orjson.dumps(json_data[0]).decode('utf-8')
    except orjson.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")

    return config_keyword

def is_text_match_keyword(keyword_string: str, text: str) -> bool:
    """
    Check if a given text matches any keyword in the keyword string.

    The function parses the keyword string into an array of keywords and checks 
    if any keyword or set of keywords (separated by spaces) is present in the text.

    Args:
        keyword_string (str): The string containing keywords to match.
        text (str): The text to check against the keywords.

    Returns:
        bool: True if the text matches any keyword or set of keywords, False otherwise.
    """
    if not keyword_string or not text:
        return False

    if not (keyword_string.startswith('"') and keyword_string.endswith('"')):
        keyword_string = f'"{keyword_string}"'

    try:
        keyword_list = orjson.loads(f"[{keyword_string}]")
    except orjson.JSONDecodeError as e:
        print(f"Invalid keyword string format: {e}")
        return False

    for keyword_group in keyword_list:
        if not keyword_group:
            return True

        if ' ' in keyword_group:
            if all(word in text for word in keyword_group.split()):
                return True
        elif keyword_group in text:
            return True

    return False

def write_string_to_file(file_path: str, data: str) -> None:
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(data)


def save_json(config_dict, target_path):
    try:
        with open(target_path, 'wb') as outfile:
            outfile.write(orjson.dumps(config_dict))
    except Exception as e:
        print(f"Failed to write to {target_path}: {e}")


def play_mp3_async(sound_filename):
    threading.Thread(target=play_mp3, args=(sound_filename,)).start()

def play_mp3(sound_filename):
    from playsound import playsound
    try:
        playsound(sound_filename)
    except Exception as exc:
        msg=str(exc)
        #print("play sound exeption:", msg)
        if platform.system() == 'Windows':
            import winsound
            try:
                winsound.PlaySound(sound_filename, winsound.SND_FILENAME)
            except Exception as exc2:
                pass


def force_remove_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f'Failed to remove file {file_path}: {e}')


def clean_uc_exe_cache() -> bool:
    """
    Clean up undetected-chromedriver's executable cache.

    Returns:
        bool: True if the cache was found and cleaned up, False otherwise.
    """
    exe_name = "chromedriver"
    if sys.platform.endswith("win32"):
        exe_name += ".exe"

    cache_dir = ""
    if sys.platform.endswith("win32"):
        cache_dir = "~/appdata/roaming/undetected_chromedriver"
    elif "LAMBDA_TASK_ROOT" in os.environ:
        cache_dir = "/tmp/undetected_chromedriver"
    elif sys.platform.startswith(("linux", "linux2")):
        cache_dir = "~/.local/share/undetected_chromedriver"
    elif sys.platform.endswith("darwin"):
        cache_dir = "~/Library/Application Support/undetected_chromedriver"
    else:
        cache_dir = "~/.undetected_chromedriver"

    cache_dir = os.path.abspath(os.path.expanduser(cache_dir))
    cache_path = pathlib.Path(cache_dir)

    files = list(cache_path.rglob("*" + exe_name + "*"))
    cache_found = bool(files)

    for file in files:
        try:
            os.unlink(str(file))
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    return cache_found

def t_or_f(value) -> bool:
    value = str(value).strip().upper()
    return 'TRUE'.startswith(value) or 'YES'.startswith(value)

def format_keyword_string(input_string: str) -> str:
    """Format a keyword string for comparison.

    Replace full-width slash and comma with half-width ones, remove full-width
    space, dollar sign, and convert to lower case.

    Args:
        input_string (str): The keyword string to be formatted.

    Returns:
        str: The formatted keyword string.
    """
    if not input_string:
        return ''

    output_string = input_string.replace('／', '/')  # full-width slash
    output_string = output_string.replace('　', '')  # full-width space
    output_string = output_string.replace(',', '')  # full-width comma
    output_string = output_string.replace('，', '')  # full-width comma
    output_string = output_string.replace('$', '')  # dollar sign
    output_string = output_string.replace(' ', '').lower()  # remove spaces and convert to lower case

    return output_string


def format_quota_string(formated_html_text: str) -> str:
    """
    Replace full-width and other special characters with half-width ones
    for easier comparison.

    Args:
        formated_html_text (str): The string to be formatted.

    Returns:
        str: The formatted string.
    """
    # Replace full-width and other special characters with half-width ones
    formated_html_text = formated_html_text.replace('「', '【')
    formated_html_text = formated_html_text.replace('『', '【')
    formated_html_text = formated_html_text.replace('〔', '【')
    formated_html_text = formated_html_text.replace('﹝', '【')
    formated_html_text = formated_html_text.replace('〈', '【')
    formated_html_text = formated_html_text.replace('《', '【')
    formated_html_text = formated_html_text.replace('［', '【')
    formated_html_text = formated_html_text.replace('〖', '【')
    formated_html_text = formated_html_text.replace('[', '【')
    formated_html_text = formated_html_text.replace('（', '【')
    formated_html_text = formated_html_text.replace('(', '【')

    formated_html_text = formated_html_text.replace('」', '】')
    formated_html_text = formated_html_text.replace('』', '】')
    formated_html_text = formated_html_text.replace('〕', '】')
    formated_html_text = formated_html_text.replace('﹞', '】')
    formated_html_text = formated_html_text.replace('〉', '】')
    formated_html_text = formated_html_text.replace('》', '】')
    formated_html_text = formated_html_text.replace('］', '】')
    formated_html_text = formated_html_text.replace('〗', '】')
    formated_html_text = formated_html_text.replace(']', '】')
    formated_html_text = formated_html_text.replace('）', '】')
    formated_html_text = formated_html_text.replace(')', '】')

    return formated_html_text

def full2half(text):
    """
    Convert a string from full-width to half-width characters.

    This function is used to convert full-width characters commonly used in
    Chinese, Japanese, and Korean texts to their half-width counterparts.
    This is useful for comparing strings that may have different character
    widths.

    Args:
        text (str): The string to be converted.
        keyword (str): The string to be converted.

    Returns:
        str: The converted string.
    """
    if not text:
        return ""

    result = []
    for char in text:
        char_code = ord(char)
        if char_code == 0x3000:  # full-width space
            char_code = 32  # half-width space
        elif 0xFF01 <= char_code <= 0xFF5E:  # full-width characters
            char_code -= 0xfee0  # convert to half-width characters
        result.append(chr(char_code))
    return ''.join(result)


def get_chinese_numeric():
    chinese_numeric_map = {
        '0': ['0', '０', 'zero', '零'],
        '1': ['1', '１', 'one', '一', '壹', '①', '❶', '⑴'],
        '2': ['2', '２', 'two', '二', '貳', '②', '❷', '⑵'],
        '3': ['3', '３', 'three', '三', '叁', '③', '❸', '⑶'],
        '4': ['4', '４', 'four', '四', '肆', '④', '❹', '⑷'],
        '5': ['5', '５', 'five', '五', '伍', '⑤', '❺', '⑸'],
        '6': ['6', '６', 'six', '六', '陸', '⑥', '❻', '⑹'],
        '7': ['7', '７', 'seven', '七', '柒', '⑦', '❼', '⑺'],
        '8': ['8', '８', 'eight', '八', '捌', '⑧', '❽', '⑻'],
        '9': ['9', '９', 'nine', '九', '玖', '⑨', '❾', '⑼']
    }
    return chinese_numeric_map

# synonymous
def synonym_dict(char):
    chinese_numeric_map = get_chinese_numeric()
    return chinese_numeric_map.get(char, [char])


def chinese_numeric_to_int(chinese_character):
    chinese_character = chinese_character.lower()  # Convert once before loop
    chinese_to_int = get_chinese_numeric()
    
    for int_value, chinese_characters in chinese_to_int.items():
        if chinese_character in chinese_characters:
            return int(int_value)
    
    return None

def normalize_chinese_numeric(keyword):
    normalized_numerals = []
    for char in keyword:
        converted_int = chinese_numeric_to_int(char)
        if converted_int is not None:
            normalized_numerals.append(str(converted_int))
    return ''.join(normalized_numerals)

def find_continuous_number(text):
    chars = "0123456789"
    return find_continuous_pattern(chars, text)

def find_continuous_text(text):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return find_continuous_pattern(chars, text)

def find_continuous_pattern(allowed_characters, text):
    """
    Find continuous pattern of allowed characters in text.

    Args:
        allowed_characters (str): The allowed characters.
        text (str): The text to search in.

    Returns:
        str: The continuous pattern of allowed characters.
    """
    pattern = []
    for char in text:
        if char in allowed_characters:
            pattern.append(char)
        elif pattern:  # stop if the first invalid character is encountered after some valid ones
            break
    return ''.join(pattern)

def is_all_alpha_or_numeric(text: str) -> bool:
    return text.isalnum()

def get_brave_bin_path() -> str:
    system = platform.system()

    if system == 'Windows':
        paths = [
            "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            os.path.expanduser('~') + "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            "D:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        ]
        for path in paths:
            if os.path.exists(path):
                return path

    elif system == 'Linux':
        return "/usr/bin/brave-browser"

    elif system == 'Darwin':
        return '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

    return ""


def dump_settings_to_maxbot_plus_extension(ext, config_dict, CONST_MAXBOT_CONFIG_FILE):
    # sync config.
    target_path = ext
    target_path = os.path.join(target_path, "data")
    target_path = os.path.join(target_path, CONST_MAXBOT_CONFIG_FILE)
    #print("save as to:", target_path)
    if os.path.isfile(target_path):
        try:
            #print("remove file:", target_path)
            os.unlink(target_path)
        except Exception as exc:
            pass

    try:
        with open(target_path, 'wb') as outfile:
            outfile.write(orjson.dumps(config_dict))
    except Exception as e:
        pass

    # add host_permissions
    target_path = ext
    target_path = os.path.join(target_path, "manifest.json")

    manifest_dict = None
    if os.path.isfile(target_path):
        try:
            with open(target_path, 'rb') as json_data:
                manifest_dict = orjson.loads(json_data.read())
        except Exception as e:
            pass

    local_remote_url_array = []
    local_remote_url = config_dict["advanced"]["remote_url"]
    if len(local_remote_url) > 0:
        try:
            # temp_remote_url_array = json.loads("["+ local_remote_url +"]")
            temp_remote_url_array = orjson.loads("["+ local_remote_url +"]")
            for remote_url in temp_remote_url_array:
                remote_url_final = remote_url + "*"
                local_remote_url_array.append(remote_url_final)
        except Exception as exc:
            pass

    if len(local_remote_url_array) > 0:
        is_manifest_changed = False
        if 'host_permissions' in manifest_dict:
            for remote_url_final in local_remote_url_array:
                if not remote_url_final in manifest_dict["host_permissions"]:
                    #print("local remote_url not in manifest:", remote_url_final)
                    manifest_dict["host_permissions"].append(remote_url_final)
                    is_manifest_changed = True

        if is_manifest_changed:
            print('\033[32min dump_settings_to_maxbot_plus_extension()\033[0m')
            # json_str = json.dumps(manifest_dict, indent=4)
            json_str = orjson.dumps(manifest_dict).decode('utf-8')
            print(f'json_str = {json_str}')
            try:
                with open(target_path, 'w') as outfile:
                    outfile.write(json_str)
            except Exception as e:
                pass


def dump_settings_to_maxblock_plus_extension(
    ext: str, config_dict: Dict[str, Any], CONST_MAXBOT_CONFIG_FILE: str, CONST_MAXBLOCK_EXTENSION_FILTER: str
) -> None:
    """
    Syncs the configuration to the MaxBlock Plus extension.

    This function writes the `config_dict` to a file at the specified `ext` path,
    and adds a domain filter to the `config_dict` before writing.

    Args:
        ext (str): The extension path where data should be saved.
        config_dict (Dict[str, Any]): The configuration dictionary to be saved.
        CONST_MAXBOT_CONFIG_FILE (str): The name of the configuration file.
        CONST_MAXBLOCK_EXTENSION_FILTER (str): The domain filter to be added to the config.

    Returns:
        None
    """
    data_path = os.path.join(ext, "data")
    os.makedirs(data_path, exist_ok=True)  # Ensure directory exists

    config_file_path = os.path.join(data_path, CONST_MAXBOT_CONFIG_FILE)

    try:
        config_file_path.unlink(missing_ok=True)  # Delete file if it exists (Python 3.8+)
    except Exception as err:
        print(f"Error removing file {config_file_path}: {err}")

    try:
        config_dict["domain_filter"] = CONST_MAXBLOCK_EXTENSION_FILTER
        with open(config_file_path, 'wb') as outfile:
            outfile.write(orjson.dumps(config_dict))
    except Exception as err:
        print(f"Error writing to {config_file_path}: {err}")


# convert web string to reg pattern
def convert_string_to_pattern(input_string: str, dynamic_length: bool = True) -> str:
    """
    Convert a string to a regular expression pattern.

    Args:
        input_string (str): The string to convert.
        dynamic_length (bool, optional): Whether to make the pattern match strings of dynamic length. Defaults to True.

    Returns:
        str: The converted regular expression pattern.
    """
    special_chars = "[]{}()<>-"
    output_list = []

    for char in input_string:
        if char in special_chars:
            output_list.append(f"\\{char}")
        elif char.isupper():
            output_list.append("[A-Z]")
        elif char.islower():
            output_list.append("[a-z]")
        elif char.isdigit():
            output_list.append("[\d]")  # No extra backslash needed

    output_string = "".join(output_list)

    if dynamic_length:
        # Use regex to replace repeated patterns dynamically
        output_string = re.sub(r"(\[A-Z\])\1+", r"\1+", output_string)
        output_string = re.sub(r"(\[a-z\])\1+", r"\1+", output_string)
        output_string = re.sub(r"(\[\d\])\1+", r"\1+", output_string)

    return output_string


def guess_answer_list_from_multi_options(tmp_text):
    show_debug_message = True    # debug.
    show_debug_message = False   # online

    options_list = []
    matched_pattern = ""
    if len(options_list) == 0:
        if '【' in tmp_text and '】' in tmp_text:
            pattern = '【.{1,4}】'
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if '(' in tmp_text and ')' in tmp_text:
            pattern = '\(.{1,4}\)'
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if '[' in tmp_text and ']' in tmp_text:
            pattern = '\[.{1,4}\]'
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if "\n" in tmp_text and ')' in tmp_text:
            pattern = "\\n.{1,4}\)"
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if "\n" in tmp_text and ']' in tmp_text:
            pattern = "\\n.{1,4}\]"
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if "\n" in tmp_text and '】' in tmp_text:
            pattern = "\\n.{1,4}】"
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if "\n" in tmp_text and ':' in tmp_text:
            pattern = "\\n.{1,4}:"
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) <= 2:
                options_list = []
            else:
                matched_pattern = pattern

    if len(options_list) == 0:
        if " " in tmp_text and '?' in tmp_text:
            if ('.' in tmp_text or ':' in tmp_text or ')' in tmp_text or ']' in tmp_text or '>' in tmp_text):
                pattern = "[ /\n\|;\.\?]{1}.{1}[\.:)\]>]{1}.{2,3}"
                options_list = re.findall(pattern, tmp_text)
                if len(options_list) <= 2:
                    options_list = []
                else:
                    formated_list = []
                    for new_item in options_list:
                        new_item = new_item.strip()
                        if new_item[:1] == ".":
                            new_item = new_item[1:]
                        if new_item[:1] == "?":
                            new_item = new_item[1:]
                        if new_item[:1] == "|":
                            new_item = new_item[1:]
                        if new_item[:1] == ";":
                            new_item = new_item[1:]
                        if new_item[:1] == "/":
                            new_item = new_item[1:]
                        new_item = new_item.strip()
                        new_item = new_item[:1]
                        formated_list.append(new_item)
                    options_list = formated_list

                    matched_pattern = pattern

    if show_debug_message:
        print("matched pattern:", matched_pattern)

    # default remove quota
    is_trim_quota = not check_answer_keep_symbol(tmp_text)
    if show_debug_message:
        print("is_trim_quota:", is_trim_quota)

    return_list = []
    if len(options_list) > 0:
        options_list_length = len(options_list)
        if show_debug_message:
            print("options_list_length:", options_list_length)
            print("options_list:", options_list)
        if options_list_length > 2:
            is_all_options_same_length = True
            options_length_count = {}
            for i in range(options_list_length-1):
                current_option_length = len(options_list[i])
                next_option_length = len(options_list[i+1])
                if current_option_length != next_option_length:
                    is_all_options_same_length = False
                if current_option_length in options_length_count:
                    options_length_count[current_option_length] += 1
                else:
                    options_length_count[current_option_length] = 1

            if show_debug_message:
                print("is_all_options_same_length:", is_all_options_same_length)

            if is_all_options_same_length:
                return_list = []
                for each_option in options_list:
                    if len(each_option) > 2:
                        if is_trim_quota:
                            return_list.append(each_option[1:-1])
                        else:
                            return_list.append(each_option)
                    else:
                        return_list.append(each_option)
            else:
                #print("options_length_count:", options_length_count)
                if len(options_length_count) > 0:
                    target_option_length = 0
                    most_length_count = 0
                    for k in options_length_count.keys():
                        if options_length_count[k] > most_length_count:
                            most_length_count = options_length_count[k]
                            target_option_length = k
                    #print("most_length_count:", most_length_count)
                    #print("target_option_length:", target_option_length)
                    if target_option_length > 0:
                        return_list = []
                        for each_option in options_list:
                            current_option_length = len(each_option)
                            if current_option_length == target_option_length:
                                if is_trim_quota:
                                    return_list.append(each_option[1:-1])
                                else:
                                    return_list.append(each_option)

    # something is wrong, give up when option equal 2 options.
    if len(return_list) <= 2:
        return_list = []

    # remove chinese work options.
    if len(options_list) > 0:
        new_list = []
        for item in return_list:
            if is_all_alpha_or_numeric(item):
                new_list.append(item)
        if len(new_list) >=3:
            return_list = new_list

    return return_list


#PS: this may get a wrong answer list. XD
def guess_answer_list_from_symbols(captcha_text_div_text):
    return_list = []
    # need replace to space to get first options.
    tmp_text = captcha_text_div_text
    tmp_text = tmp_text.replace('?',' ')
    tmp_text = tmp_text.replace('？',' ')
    tmp_text = tmp_text.replace('。',' ')

    delimitor_symbols_left = [u"(","[","{", " ", " ", " ", " "]
    delimitor_symbols_right = [u")","]","}", ":", ".", ")", "-"]
    idx = -1
    for idx in range(len(delimitor_symbols_left)):
        symbol_left = delimitor_symbols_left[idx]
        symbol_right = delimitor_symbols_right[idx]
        if symbol_left in tmp_text and symbol_right in tmp_text and '半形' in tmp_text:
            hint_list = re.findall('\\'+ symbol_left + '[\\w]+\\'+ symbol_right , tmp_text)
            #print("hint_list:", hint_list)
            if not hint_list is None:
                if len(hint_list) > 1:
                    return_list = []
                    my_answer_delimitor = symbol_right
                    for options in hint_list:
                        if len(options) > 2:
                            my_anwser = options[1:-1]
                            #print("my_anwser:",my_anwser)
                            if len(my_anwser) > 0:
                                return_list.append(my_anwser)

        if len(return_list) > 0:
            break
    return return_list

def get_offical_hint_string_from_symbol(symbol, tmp_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    offical_hint_string = ""
    if symbol in tmp_text:
        # start to guess offical hint
        if offical_hint_string == "":
            if '【' in tmp_text and '】' in tmp_text:
                hint_list = re.findall('【.*?】', tmp_text)
                if not hint_list is None:
                    if show_debug_message:
                        print("【.*?】hint_list:", hint_list)
                    for hint in hint_list:
                        if symbol in hint:
                            offical_hint_string = hint[1:-1]
                            break
        if offical_hint_string == "":
            if '(' in tmp_text and ')' in tmp_text:
                hint_list = re.findall('\(.*?\)', tmp_text)
                if not hint_list is None:
                    if show_debug_message:
                        print("\(.*?\)hint_list:", hint_list)
                    for hint in hint_list:
                        if symbol in hint:
                            offical_hint_string = hint[1:-1]
                            break
        if offical_hint_string == "":
            if '[' in tmp_text and ']' in tmp_text:
                hint_list = re.findall('[.*?]', tmp_text)
                if not hint_list is None:
                    if show_debug_message:
                        print("[.*?]hint_list:", hint_list)
                    for hint in hint_list:
                        if symbol in hint:
                            offical_hint_string = hint[1:-1]
                            break
        if offical_hint_string == "":
            offical_hint_string = tmp_text
    return offical_hint_string


def guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

    my_question = ""
    my_options = ""
    offical_hint_string = ""
    offical_hint_string_anwser = ""
    my_anwser_formated = ""
    my_answer_delimitor = ""

    if my_question == "":
        if "?" in tmp_text:
            question_index = tmp_text.find("?")
            my_question = tmp_text[:question_index+1]
    if my_question == "":
        if "。" in tmp_text:
            question_index = tmp_text.find("。")
            my_question = tmp_text[:question_index+1]
    if my_question == "":
        my_question = tmp_text
    #print("my_question:", my_question)

    # ps: hint_list is not options list

    if offical_hint_string == "":
        # for: 若你覺得答案為 a，請輸入 a
        if '答案' in tmp_text and CONST_INPUT_SYMBOL in tmp_text:
            offical_hint_string = get_offical_hint_string_from_symbol(CONST_INPUT_SYMBOL, tmp_text)
        if len(offical_hint_string) > 0:
            right_part = offical_hint_string.split(CONST_INPUT_SYMBOL)[1]
            #print("right_part:", right_part)
            if len(offical_hint_string) == len(tmp_text):
                offical_hint_string = right_part

            new_hint = find_continuous_text(right_part)
            if len(new_hint) > 0:
                # TODO: 答案為B需填入Bb)
                #if '答案' in offical_hint_string and CONST_INPUT_SYMBOL in offical_hint_string:
                offical_hint_string_anwser = new_hint


    if offical_hint_string == "":
        offical_hint_string = get_offical_hint_string_from_symbol(CONST_EXAMPLE_SYMBOL, tmp_text)
        if len(offical_hint_string) > 0:
            right_part = offical_hint_string.split(CONST_EXAMPLE_SYMBOL)[1]
            if len(offical_hint_string) == len(tmp_text):
                offical_hint_string = right_part

            # PS: find first text will only get B char in this case: 答案為B需填入Bb)
            new_hint = find_continuous_text(right_part)
            if len(new_hint) > 0:
                offical_hint_string_anwser = new_hint

    # resize offical_hint_string_anwser for options contains in hint string.
    #print("offical_hint_string_anwser:", offical_hint_string_anwser)
    if len(offical_hint_string_anwser) > 0:
        offical_hint_string = offical_hint_string.split(offical_hint_string_anwser)[0]

    if show_debug_message:
        print("offical_hint_string:", offical_hint_string)

    # try rule4:
    # get hint from rule 3: without '(' & '), but use "*"
    if len(offical_hint_string) == 0:
        target_symbol = "*"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index + len(target_symbol))
            offical_hint_string = tmp_text[star_index: space_index]

    # is need to merge next block
    if len(offical_hint_string) > 0:
        target_symbol = offical_hint_string + " "
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            next_block_index = star_index + len(target_symbol)
            space_index = tmp_text.find(" ", next_block_index)
            next_block = tmp_text[next_block_index: space_index]
            if CONST_EXAMPLE_SYMBOL in next_block:
                offical_hint_string += ' ' + next_block

    # try rule5:
    # get hint from rule 3: n個半形英文大寫
    if len(offical_hint_string) == 0:
        target_symbol = "個半形英文大寫"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                offical_hint_string_anwser = 'A' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

        target_symbol = "個英文大寫"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                offical_hint_string_anwser = 'A' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

        target_symbol = "個半形英文小寫"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                offical_hint_string_anwser = 'a' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

        target_symbol = "個英文小寫"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                offical_hint_string_anwser = 'a' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

        target_symbol = "個英數半形字"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                my_anwser_formated = '[A-Za-z\d]' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

        target_symbol = "個半形"
        if target_symbol in tmp_text :
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index-1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count =  chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'

                star_index -= 1
                my_anwser_formated = '[A-Za-z\d]' * int(answer_char_count)
            offical_hint_string = tmp_text[star_index: space_index]

    if len(offical_hint_string) > 0:
        if show_debug_message:
            print("offical_hint_string_anwser:", offical_hint_string_anwser)
        my_anwser_formated = convert_string_to_pattern(offical_hint_string_anwser)

    my_options = tmp_text
    if len(my_question) < len(tmp_text):
        my_options = my_options.replace(my_question,"")
    my_options = my_options.replace(offical_hint_string,"")

    # try rule7:
    # check is chinese/english in question, if match, apply my_options rule.
    if len(offical_hint_string) > 0:
        tmp_text_org = captcha_text_div_text
        if CONST_EXAMPLE_SYMBOL in tmp_text:
            tmp_text_org = tmp_text_org.replace('Ex:','ex:')
            target_symbol = "ex:"
            if target_symbol in tmp_text_org :
                star_index = tmp_text_org.find(target_symbol)
                my_options = tmp_text_org[star_index-1:]

    if show_debug_message:
        print("tmp_text:", tmp_text)
        print("my_options:", my_options)

    if len(my_anwser_formated) > 0:
        allow_delimitor_symbols = ")].: }"
        pattern = re.compile(my_anwser_formated)
        search_result = pattern.search(my_options)
        if not search_result is None:
            (span_start, span_end) = search_result.span()
            maybe_delimitor=""
            if len(my_options) > (span_end+1)+1:
                maybe_delimitor = my_options[span_end+0:span_end+1]
            if maybe_delimitor in allow_delimitor_symbols:
                my_answer_delimitor = maybe_delimitor

    if show_debug_message:
        print("my_answer_delimitor:", my_answer_delimitor)

    # default remove quota
    is_trim_quota = not check_answer_keep_symbol(tmp_text)
    if show_debug_message:
        print("is_trim_quota:", is_trim_quota)

    return_list = []
    if len(my_anwser_formated) > 0:
        new_pattern = my_anwser_formated
        if len(my_answer_delimitor) > 0:
            new_pattern = my_anwser_formated + '\\' + my_answer_delimitor

        return_list = re.findall(new_pattern, my_options)
        if show_debug_message:
            print("my_anwser_formated:", my_anwser_formated)
            print("new_pattern:", new_pattern)
            print("return_list:" , return_list)

        if not return_list is None:
            if len(return_list) == 1:
                # re-sample for this case.
                return_list = re.findall(my_anwser_formated, my_options)

            if len(return_list) == 1:
                # if use pattern to find matched only one, means it is for example text.
                return_list = None

        if not return_list is None:
            # clean delimitor
            if is_trim_quota:
                return_list_length = len(return_list)
                if return_list_length >= 1:
                    if len(my_answer_delimitor) > 0:
                        for idx in range(return_list_length):
                            return_list[idx]=return_list[idx].replace(my_answer_delimitor,'')
                if show_debug_message:
                    print("cleaned return_list:" , return_list)

        if return_list is None:
            return_list = []

    return return_list, offical_hint_string_anwser


def format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text):
    """
    Formats the given captcha text by replacing certain characters and phrases
    with specified symbols and removing unnecessary words.

    Args:
        example_symbol (str): The symbol to replace example indicators.
        input_symbol (str): The symbol to replace input indicators.
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    if not captcha_text_div_text:
        return captcha_text_div_text

    text = re.sub(r'\s+', ' ', captcha_text_div_text.strip())

    # Replace double spaces and specific characters
    text = text.translate(str.maketrans({'：': ':', '？': '?', '（': '(', '）': ')'}))

    # Remove stopped words
    stop_words = ['輸入法', '請問', '請將', '請在', '請以', '請回答', '請']
    text = re.sub('|'.join(stop_words), '', text)

    # Replace example indicators
    example_phrases = ['例如', '如:', '如為', '舉例', '例', 'ex:', 'Ex:']
    text = re.sub('|'.join(example_phrases), CONST_EXAMPLE_SYMBOL, text)

    # Replace conditional phrases related to answers
    conditional_phrases = ['假設', '如果', '若']
    if '答案' in text:
        text = re.sub(r'覺得|認為', '', text)
        for phrase in conditional_phrases:
            text = text.replace(f'{phrase}你答案', f'{CONST_EXAMPLE_SYMBOL}答案')
            text = text.replace(f'{phrase}答案', f'{CONST_EXAMPLE_SYMBOL}答案')

    # Replace input indicators
    text = text.replace('填入', CONST_INPUT_SYMBOL)

    return text

def permutations(iterable, r=None):
    """
    Generate permutations of an iterable.

    Args:
        iterable (iterable): The input iterable to generate permutations from.
        r (int, optional): The length of each permutation tuple. Defaults to the length of the iterable.

    Example:
        >>> for perm in permutations([1, 2, 3]):
        ...     print(perm)
        (1, 2, 3)
        (1, 3, 2)
        (2, 1, 3)
        (2, 3, 1)
        (3, 1, 2)
        (3, 2, 1)

    If r is None, generate permutations of the full length of the iterable.
    """
    if r is None:
        r = len(iterable)

    from itertools import permutations
    return permutations(iterable, r)

def get_answer_list_by_question(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text):
    show_debug_message = True    # debug.
    show_debug_message = False   # online

    return_list = []

    tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

    # guess answer list from multi-options: 【】() []
    if len(return_list)==0:
        return_list = guess_answer_list_from_multi_options(tmp_text)
    if show_debug_message:
        print("captcha_text_div_text:", captcha_text_div_text)
        if len(return_list) > 0:
            print("found, guess_answer_list_from_multi_options:", return_list)

    offical_hint_string_anwser = ""
    if len(return_list)==0:
        return_list, offical_hint_string_anwser = guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)
    else:
        is_match_factorial = False
        mutiple = 0

        return_list_2, offical_hint_string_anwser = guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)
        if return_list_2 is None:
            if len(offical_hint_string_anwser) >=3:
                if len(return_list) >=3:
                    mutiple = int(len(offical_hint_string_anwser) / len(return_list[0]))
                    if mutiple >=3 :
                        is_match_factorial = True

        if show_debug_message:
            print("mutiple:", mutiple)
            print("is_match_factorial:", is_match_factorial)
        if is_match_factorial:
            is_match_factorial = False
            order_string_list = ['排列','排序','依序','順序','遞增','遞減','升冪','降冪','新到舊','舊到新','小到大','大到小','高到低','低到高']
            for order_string in order_string_list:
                if order_string in tmp_text:
                    is_match_factorial = True

        if is_match_factorial:
            new_array = permutations(return_list, mutiple)
            #print("new_array:", new_array)

            return_list = []
            for item_tuple in new_array:
                return_list.append(''.join(item_tuple))

        if show_debug_message:
            if len(return_list) > 0:
                print("found, guess_answer_list_from_hint:", return_list)

    if len(return_list)==0:
        return_list = guess_answer_list_from_symbols(captcha_text_div_text)
        if show_debug_message:
            if len(return_list) > 0:
                print("found, guess_answer_list_from_symbols:", return_list)

    return return_list


def get_matched_blocks_by_keyword_item_set(config_dict, auto_select_mode, keyword_item_set, formated_area_list):
    show_debug_message = True    # debug.
    show_debug_message = False   # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

    matched_blocks = []
    for row in formated_area_list:
        row_text = ""
        row_html = ""
        try:
            #row_text = row.text
            row_html = row.get_attribute('innerHTML')
            row_text = remove_html_tags(row_html)
        except Exception as exc:
            if show_debug_message:
                print(exc)
            # error, exit loop
            break

        if len(row_text) > 0:
            if reset_row_text_if_match_keyword_exclude(config_dict, row_text):
                row_text = ""

        if len(row_text) > 0:
            # start to compare, normalize all.
            row_text = format_keyword_string(row_text)
            if show_debug_message:
                print("row_text:", row_text)

            is_match_all = False
            if ' ' in keyword_item_set:
                keyword_item_array = keyword_item_set.split(' ')
                is_match_all = True
                for keyword_item in keyword_item_array:
                    keyword_item = format_keyword_string(keyword_item)
                    if not keyword_item in row_text:
                        is_match_all = False
            else:
                exclude_item = format_keyword_string(keyword_item_set)
                if exclude_item in row_text:
                    is_match_all = True

            if is_match_all:
                matched_blocks.append(row)

                # only need first row.
                if auto_select_mode == CONST_FROM_TOP_TO_BOTTOM:
                    break
    return matched_blocks

def get_target_item_from_matched_list(matched_blocks, auto_select_mode):
    if matched_blocks is None:
        return None

    target_area = None
    matched_blocks_count = len(matched_blocks)
    if matched_blocks_count > 0:
        target_row_index = 0

        # if auto_select_mode == CONST_FROM_TOP_TO_BOTTOM:
        #     pass

        if auto_select_mode == CONST_FROM_BOTTOM_TO_TOP:
            target_row_index = matched_blocks_count - 1

        if auto_select_mode == CONST_RANDOM and matched_blocks_count > 1:
                target_row_index = random.randint(0,matched_blocks_count-1)

        if auto_select_mode == CONST_CENTER and matched_blocks_count > 2:
                target_row_index = int(matched_blocks_count/2)

        target_area = matched_blocks[target_row_index]
    return target_area


def get_matched_blocks_by_keyword(config_dict, auto_select_mode, keyword_string, formated_area_list):
    try:
        # keyword_array = json.loads("["+ keyword_string +"]")
        keyword_array = orjson.loads("["+ keyword_string +"]")
    except orjson.JSONDecodeError:
        return []

    for keyword_item_set in keyword_array:
        matched_blocks = get_matched_blocks_by_keyword_item_set(config_dict, auto_select_mode, keyword_item_set, formated_area_list)
        if matched_blocks:
            return matched_blocks
    return []


def is_row_match_keyword(keyword_string, row_text):
    # clean stop word.
    row_text = format_keyword_string(row_text)

    is_match_keyword = True
    if len(keyword_string) > 0 and len(row_text) > 0:
        is_match_keyword = False
        keyword_array = []
        try:
            # keyword_array = json.loads("["+ keyword_string +"]")
            keyword_array = orjson.loads("["+ keyword_string +"]")
        except Exception as exc:
            keyword_array = []
        for item_list in keyword_array:
            if len(item_list) > 0:
                if ' ' in item_list:
                    keyword_item_array = item_list.split(' ')
                    is_match_all_exclude = True
                    for each_item in keyword_item_array:
                        each_item = format_keyword_string(each_item)
                        if not each_item in row_text:
                            is_match_all_exclude = False
                    if is_match_all_exclude:
                        is_match_keyword = True
                else:
                    item_list = format_keyword_string(item_list)
                    if item_list in row_text:
                        is_match_keyword = True
            else:
                # match all.
                is_match_keyword = True
            if is_match_keyword:
                break
    return is_match_keyword

def reset_row_text_if_match_keyword_exclude(config_dict, row_text):
    area_keyword_exclude = config_dict["keyword_exclude"]
    return is_row_match_keyword(area_keyword_exclude, row_text)


def guess_tixcraft_question(driver, question_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    answer_list = []

    formated_html_text = ""
    if len(question_text) > 0:
        # format question text.
        formated_html_text = question_text
        formated_html_text = format_quota_string(formated_html_text)

        if '【' in formated_html_text and '】' in formated_html_text:
            # PS: 這個太容易沖突，因為問題類型太多，不能直接使用。
            #inferred_answer_string = find_between(formated_html_text, "【", "】")
            pass

    if show_debug_message:
        print("formated_html_text:", formated_html_text)

    # start to guess answer
    inferred_answer_string = None

    # 請輸入"YES"，代表您已詳閱且瞭解並同意。
    if inferred_answer_string is None:
        if '輸入"YES"' in formated_html_text:
            if '已詳閱' in formated_html_text or '請詳閱' in formated_html_text:
                if '同意' in formated_html_text:
                    inferred_answer_string = 'YES'

    # 購票前請詳閱注意事項，並於驗證碼欄位輸入【同意】繼續購票流程。
    if inferred_answer_string is None:
        if '驗證碼' in formated_html_text or '驗證欄位' in formated_html_text:
            if '已詳閱' in formated_html_text or '請詳閱' in formated_html_text:
                if '輸入【同意】' in formated_html_text:
                    inferred_answer_string = '同意'

    if inferred_answer_string is None:
        if len(question_text) > 0:
            answer_list = get_answer_list_from_question_string(None, question_text)
    else:
        answer_list = [answer_list]

    return answer_list

def get_answer_list_from_user_guess_string(config_dict, CONST_MAXBOT_ANSWER_ONLINE_FILE):
    local_array = []
    online_array = []

    user_guess_string = config_dict["advanced"]["user_guess_string"]
    if len(user_guess_string) > 0:
        user_guess_string = format_config_keyword_for_json(user_guess_string)
        try:
            # local_array = json.loads("["+ user_guess_string +"]")
            local_array = orjson.loads("["+ user_guess_string +"]")
        except Exception as exc:
            local_array = []

    # load from internet.
    user_guess_string = ""
    if os.path.exists(CONST_MAXBOT_ANSWER_ONLINE_FILE):
        try:
            with open(CONST_MAXBOT_ANSWER_ONLINE_FILE, "r") as text_file:
                user_guess_string = text_file.readline()
        except Exception as e:
            pass

    if len(user_guess_string) > 0:
        user_guess_string = format_config_keyword_for_json(user_guess_string)
        try:
            # online_array = json.loads("["+ user_guess_string +"]")
            online_array = orjson.loads("["+ user_guess_string +"]")
        except Exception as exc:
            online_array = []

    return local_array + online_array

def check_answer_keep_symbol(captcha_text_div_text):
    is_need_keep_symbol = False

    # format text
    keep_symbol_tmp = captcha_text_div_text
    keep_symbol_tmp = keep_symbol_tmp.replace('也','須')
    keep_symbol_tmp = keep_symbol_tmp.replace('必須','須')

    keep_symbol_tmp = keep_symbol_tmp.replace('全都','都')
    keep_symbol_tmp = keep_symbol_tmp.replace('全部都','都')

    keep_symbol_tmp = keep_symbol_tmp.replace('一致','相同')
    keep_symbol_tmp = keep_symbol_tmp.replace('一樣','相同')
    keep_symbol_tmp = keep_symbol_tmp.replace('相等','相同')

    if '符號須都相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    if '符號都相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    if '符號須相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    # for: 大小寫含括號需一模一樣
    keep_symbol_tmp = keep_symbol_tmp.replace('含', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('和', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('與', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('還有', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('及', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('以及', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('需', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('必須', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('而且', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('且', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('一模', '')
    #print("keep_symbol_tmp:", keep_symbol_tmp)
    if '大小寫括號相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    return is_need_keep_symbol

#PS: this is for selenium webdriver.
def kktix_get_web_datetime(registrationsNewApp_div):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    web_datetime = None

    is_found_web_datetime = False

    el_web_datetime_list = None
    if not registrationsNewApp_div is None:
        try:
            el_web_datetime_list = registrationsNewApp_div.find_elements(By.TAG_NAME, 'td')
        except Exception as exc:
            if show_debug_message:
                print("find td.ng-binding Exception")
                print(exc)
            pass
        #print("is_found_web_datetime", is_found_web_datetime)

    if not el_web_datetime_list is None:
        el_web_datetime_list_count = len(el_web_datetime_list)
        if el_web_datetime_list_count > 0:
            el_web_datetime = None
            for el_web_datetime in el_web_datetime_list:
                el_web_datetime_text = None
                try:
                    el_web_datetime_text = el_web_datetime.text
                    if show_debug_message:
                        print("el_web_datetime_text:", el_web_datetime_text)
                except Exception as exc:
                    if show_debug_message:
                        print('parse web datetime fail:')
                        print(exc)
                    pass

                if not el_web_datetime_text is None:
                    if len(el_web_datetime_text) > 0:
                        now = datetime.now()
                        #print("now:", now)
                        for guess_year in range(now.year,now.year+3):
                            current_year = str(guess_year)
                            if current_year in el_web_datetime_text:
                                if '/' in el_web_datetime_text:
                                    web_datetime = el_web_datetime_text
                                    is_found_web_datetime = True
                                    break
                        if is_found_web_datetime:
                            break
    else:
        print("find td.ng-binding fail")

    if show_debug_message:
        print('is_found_web_datetime:', is_found_web_datetime)
        print('web_datetime:', web_datetime)

    return web_datetime

def get_answer_string_from_web_date(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div, captcha_text_div_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    inferred_answer_string = None

    is_need_parse_web_datetime = False
    # '半形阿拉伯數字' & '半形數字'
    if '半形' in captcha_text_div_text and '字' in captcha_text_div_text:
        if '演出日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '活動日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '表演日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '開始日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '演唱會日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '展覽日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '音樂會日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
    if 'the date of the show you purchased' in captcha_text_div_text:
        is_need_parse_web_datetime = True

    if show_debug_message:
        print("is_need_parse_web_datetime:", is_need_parse_web_datetime)

    if is_need_parse_web_datetime:
        web_datetime = kktix_get_web_datetime(registrationsNewApp_div)
        if not web_datetime is None:
            if show_debug_message:
                print("web_datetime:", web_datetime)

            captcha_text_formatted = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)
            if show_debug_message:
                print("captcha_text_formatted", captcha_text_formatted)

            my_datetime_foramted = None

            # MMDD
            if my_datetime_foramted is None:
                if '4位半形' in captcha_text_formatted:
                    my_datetime_foramted = "%m%d"

            # for "如為2月30日，請輸入0230"
            if my_datetime_foramted is None:
                right_part = ""
                if CONST_EXAMPLE_SYMBOL in captcha_text_formatted:
                    right_part = captcha_text_formatted.split(CONST_EXAMPLE_SYMBOL)[1]

                if CONST_INPUT_SYMBOL in right_part:
                    right_part = right_part.split(CONST_INPUT_SYMBOL)[1]
                    number_text = find_continuous_number(right_part)

                    my_anwser_formated = convert_string_to_pattern(number_text, dynamic_length=False)
                    if my_anwser_formated == "[\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d]":
                        my_datetime_foramted = "%Y%m%d"
                    if my_anwser_formated == "[\\d][\\d][\\d][\\d]":
                        my_datetime_foramted = "%m%d"
                    #print("my_datetime_foramted:", my_datetime_foramted)

            if show_debug_message:
                print("my_datetime_foramted", my_datetime_foramted)

            if my_datetime_foramted is None:
                now = datetime.now()
                for guess_year in range(now.year-4,now.year+2):
                    current_year = str(guess_year)
                    if current_year in captcha_text_formatted:
                        my_hint_index = captcha_text_formatted.find(current_year)
                        my_hint_anwser = captcha_text_formatted[my_hint_index:]
                        #print("my_hint_anwser:", my_hint_anwser)
                        # get after.
                        my_delimitor_symbol = CONST_EXAMPLE_SYMBOL
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[my_delimitor_index+len(my_delimitor_symbol):]
                        #print("my_hint_anwser:", my_hint_anwser)
                        # get before.
                        my_delimitor_symbol = '，'
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        my_delimitor_symbol = '。'
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        # PS: space may not is delimitor...
                        my_delimitor_symbol = ' '
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        #remove last char.
                        remove_last_char_list = [')','(','.','。','）','（','[',']']
                        for check_char in remove_last_char_list:
                            if my_hint_anwser[-1:]==check_char:
                                my_hint_anwser = my_hint_anwser[:-1]

                        my_anwser_formated = convert_string_to_pattern(my_hint_anwser, dynamic_length=False)
                        if my_anwser_formated == "[\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d]":
                            my_datetime_foramted = "%Y%m%d"
                        if my_anwser_formated == "[\\d][\\d][\\d][\\d]/[\\d][\\d]/[\\d][\\d]":
                            my_datetime_foramted = "%Y/%m/%d"

                        if show_debug_message:
                            print("my_hint_anwser:", my_hint_anwser)
                            print("my_anwser_formated:", my_anwser_formated)
                            print("my_datetime_foramted:", my_datetime_foramted)
                        break

            if not my_datetime_foramted is None:
                my_delimitor_symbol = ' '
                if my_delimitor_symbol in web_datetime:
                    web_datetime = web_datetime[:web_datetime.find(my_delimitor_symbol)]
                date_time = datetime.strptime(web_datetime,"%Y/%m/%d")
                if show_debug_message:
                    print("our web date_time:", date_time)
                ans = None
                try:
                    if not date_time is None:
                        ans = date_time.strftime(my_datetime_foramted)
                except Exception as exc:
                    pass
                inferred_answer_string = ans
                if show_debug_message:
                    print("web date_time anwser:", ans)

    return inferred_answer_string

def get_answer_string_from_web_time(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div, captcha_text_div_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    inferred_answer_string = None

    # parse '演出時間'
    is_need_parse_web_time = False
    if '半形' in captcha_text_div_text:
        if '演出時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '表演時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '開始時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '演唱會時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '展覽時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '音樂會時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if 'the time of the show you purchased' in captcha_text_div_text:
            is_need_parse_web_time = True

    #print("is_need_parse_web_time", is_need_parse_web_time)
    if is_need_parse_web_time:
        web_datetime = None
        if not registrationsNewApp_div is None:
            web_datetime = kktix_get_web_datetime(registrationsNewApp_div)
        if not web_datetime is None:
            tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

            my_datetime_foramted = None

            if my_datetime_foramted is None:
                my_hint_anwser = tmp_text

                my_delimitor_symbol = CONST_EXAMPLE_SYMBOL
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[my_delimitor_index+len(my_delimitor_symbol):]
                #print("my_hint_anwser:", my_hint_anwser)
                # get before.
                my_delimitor_symbol = '，'
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                my_delimitor_symbol = '。'
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                # PS: space may not is delimitor...
                my_delimitor_symbol = ' '
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                my_anwser_formated = convert_string_to_pattern(my_hint_anwser, dynamic_length=False)
                #print("my_hint_anwser:", my_hint_anwser)
                #print("my_anwser_formated:", my_anwser_formated)
                if my_anwser_formated == "[\\d][\\d][\\d][\\d]":
                    my_datetime_foramted = "%H%M"
                    if '12小時' in tmp_text:
                        my_datetime_foramted = "%I%M"

                if my_anwser_formated == "[\\d][\\d]:[\\d][\\d]":
                    my_datetime_foramted = "%H:%M"
                    if '12小時' in tmp_text:
                        my_datetime_foramted = "%I:%M"

            if not my_datetime_foramted is None:
                date_delimitor_symbol = '('
                if date_delimitor_symbol in web_datetime:
                    date_delimitor_symbol_index = web_datetime.find(date_delimitor_symbol)
                    if date_delimitor_symbol_index > 8:
                        web_datetime = web_datetime[:date_delimitor_symbol_index-1]
                date_time = datetime.strptime(web_datetime,"%Y/%m/%d %H:%M")
                #print("date_time:", date_time)
                ans = None
                try:
                    ans = date_time.strftime(my_datetime_foramted)
                except Exception as exc:
                    pass
                inferred_answer_string = ans
                #print("my_anwser:", ans)

    return inferred_answer_string

def get_answer_list_from_question_string(registrationsNewApp_div, captcha_text_div_text):
    show_debug_message = True       # debug.
    show_debug_message = False      # online

    inferred_answer_string = None
    answer_list = []

    CONST_EXAMPLE_SYMBOL = "範例"
    CONST_INPUT_SYMBOL = "輸入"

    if captcha_text_div_text is None:
        captcha_text_div_text = ""

    # 請在下方空白處輸入引號內文字：
    # 請回答下列問題,請在下方空格輸入DELIGHT（請以半形輸入法作答，大小寫需要一模一樣）
    if inferred_answer_string is None:
        is_use_quota_message = False
        if "「" in captcha_text_div_text and "」" in captcha_text_div_text:
            # test for rule#1, it's seem very easy conflict...
            match_quota_text_items = ["空白","輸入","引號","文字"]
            is_match_quota_text = True
            for each_quota_text in match_quota_text_items:
                if not each_quota_text in captcha_text_div_text:
                    is_match_quota_text = False
            if is_match_quota_text:
                is_use_quota_message = True
        #print("is_use_quota_message:" , is_use_quota_message)
        if is_use_quota_message:
            temp_answer = find_between(captcha_text_div_text, "「", "」")
            temp_answer = temp_answer.strip()
            if len(temp_answer) > 0:
                inferred_answer_string = temp_answer
            #print("find captcha text:" , inferred_answer_string)

    # 請在下方空白處輸入括號內數字
    if inferred_answer_string is None:
        formated_html_text = captcha_text_div_text.strip()
        formated_html_text = format_quota_string(formated_html_text)
        formated_html_text = formated_html_text.replace('請輸入','輸入')

        formated_html_text = formated_html_text.replace('的','')
        formated_html_text = formated_html_text.replace('之內','內')
        formated_html_text = formated_html_text.replace('之中','中')

        formated_html_text = formated_html_text.replace('括弧','括號')
        formated_html_text = formated_html_text.replace('引號','括號')

        formated_html_text = formated_html_text.replace('括號中','括號內')

        formated_html_text = formated_html_text.replace('數字','文字')

        is_match_input_quota_text = False
        if len(formated_html_text) <= 30:
            if not '\n' in formated_html_text:
                if '【' in formated_html_text and '】' in formated_html_text:
                    is_match_input_quota_text = True

        # check target text terms.
        if is_match_input_quota_text:
            target_text_list = ["輸入","括號","文字"]
            for item in target_text_list:
                if not item in formated_html_text:
                    is_match_input_quota_text = False
                    break

        if is_match_input_quota_text:
            temp_answer = find_between(formated_html_text, "【", "】")
            temp_answer = temp_answer.strip()
            if len(temp_answer) > 0:
                temp_answer = temp_answer.replace(' ','')

                # check raw question.
                if '數字' in captcha_text_div_text:
                    temp_answer = normalize_chinese_numeric(temp_answer)

                inferred_answer_string = temp_answer

    if inferred_answer_string is None:
        is_use_quota_message = False
        if "【" in captcha_text_div_text and "】" in captcha_text_div_text:
            if '下' in captcha_text_div_text and '空' in captcha_text_div_text and CONST_INPUT_SYMBOL in captcha_text_div_text and '引號' in captcha_text_div_text and '字' in captcha_text_div_text:
                is_use_quota_message = True
            if '半形' in captcha_text_div_text and CONST_INPUT_SYMBOL in captcha_text_div_text and '引號' in captcha_text_div_text and '字' in captcha_text_div_text:
                is_use_quota_message = True
        #print("is_use_quota_message:" , is_use_quota_message)
        if is_use_quota_message:
            inferred_answer_string = find_between(captcha_text_div_text, "【", "】")
            inferred_answer_string = inferred_answer_string.strip()
            #print("find captcha text:" , inferred_answer_string)

    # parse '演出日期'
    if inferred_answer_string is None:
        inferred_answer_string = get_answer_string_from_web_date(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div, captcha_text_div_text)

    # parse '演出時間'
    if inferred_answer_string is None:
        inferred_answer_string = get_answer_string_from_web_time(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div, captcha_text_div_text)

    # name of event.
    if inferred_answer_string is None:
        if "name of event" in captcha_text_div_text:
            if '(' in captcha_text_div_text and ')' in captcha_text_div_text and 'ans:' in captcha_text_div_text.lower():
                target_symbol = "("
                star_index = captcha_text_div_text.find(target_symbol)
                target_symbol = ":"
                star_index = captcha_text_div_text.find(target_symbol, star_index)
                target_symbol = ")"
                end_index = captcha_text_div_text.find(target_symbol, star_index)
                inferred_answer_string = captcha_text_div_text[star_index+1:end_index]
                #print("inferred_answer_string:", inferred_answer_string)

    # 二題式，組合問題。
    is_combine_two_question = False
    if "第一題" in captcha_text_div_text and "第二題" in captcha_text_div_text:
        is_combine_two_question = True
    if "Q1." in captcha_text_div_text and "Q2." in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if "Q1:" in captcha_text_div_text and "Q2:" in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if "Q1 " in captcha_text_div_text and "Q2 " in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if is_combine_two_question:
        inferred_answer_string = None
    #print("is_combine_two_question:", is_combine_two_question)

    # still no answer.
    if inferred_answer_string is None:
        if not is_combine_two_question:
            answer_list = get_answer_list_by_question(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)
            if show_debug_message:
                print("guess answer list:", answer_list)
        else:
            if show_debug_message:
                print("skip to guess answer because of combine question...")

    else:
        if show_debug_message:
            print("got an inferred_answer_string:", inferred_answer_string)
        answer_list = [inferred_answer_string]

    return answer_list

def kktix_get_registerStatus(event_code):
    html_result = None

    url = "https://kktix.com/g/events/%s/register_info" % (event_code)
    #print('event_code:',event_code)
    #print("url:", url)

    headers = {"Accept-Language": "zh-TW,zh;q=0.5", 'User-Agent': USER_AGENT}
    try:
        html_result = requests.get(url , headers=headers, timeout=0.7, allow_redirects=False)
    except Exception as exc:
        html_result = None
        print("send reg_info request fail:")
        print(exc)

    registerStatus = ""
    if not html_result is None:
        status_code = html_result.status_code
        #print("status_code:",status_code)
        if status_code == 200:
            html_text = html_result.text
            #print("html_text:", html_text)
            try:
                # jsLoads = json.loads(html_text)
                jsLoads = orjson.loads(html_text)
                if 'inventory' in jsLoads:
                    if 'registerStatus' in jsLoads['inventory']:
                        registerStatus = jsLoads['inventory']['registerStatus']
            except Exception as exc:
                print("load reg_info json fail:")
                print(exc)
                pass

    #print("registerStatus:", registerStatus)
    return registerStatus

def kktix_get_event_code(url):
    event_code = ""
    if '/registrations/new' in url:
        prefix_list = ['.com/events/','.cc/events/']
        postfix = '/registrations/new'

        for prefix in prefix_list:
            event_code = find_between(url,prefix,postfix)
            if len(event_code) > 0:
                break

    #print('event_code:',event_code)
    return event_code

def get_kktix_status_by_url(url):
    registerStatus = ""
    if len(url) > 0:
        event_code = kktix_get_event_code(url)
        #print(event_code)
        if len(event_code) > 0:
            registerStatus = kktix_get_registerStatus(event_code)
            #print(registerStatus)
    return registerStatus

def launch_maxbot(script_name="chrome_tixcraft", filename="", homepage="", kktix_account = "", kktix_password="", window_size="", headless=""):
    cmd_argument = []
    if len(filename) > 0:
        cmd_argument.append('--input=' + filename)
    if len(homepage) > 0:
        cmd_argument.append('--homepage=' + homepage)
    if len(kktix_account) > 0:
        cmd_argument.append('--kktix_account=' + kktix_account)
    if len(kktix_password) > 0:
        cmd_argument.append('--kktix_password=' + kktix_password)
    if len(window_size) > 0:
        cmd_argument.append('--window_size=' + window_size)
    if len(headless) > 0:
        cmd_argument.append('--headless=' + headless)

    working_dir = os.path.dirname(os.path.realpath(__file__))
    if hasattr(sys, 'frozen'):
        print("execute in frozen mode")
        # check platform here.
        cmd = './' + script_name + ' '.join(cmd_argument)
        if platform.system() == 'Darwin':
            print("execute MacOS python script")
        if platform.system() == 'Linux':
            print("execute linux binary")
        if platform.system() == 'Windows':
            print("execute .exe binary.")
            cmd = script_name + '.exe ' + ' '.join(cmd_argument)
        subprocess.Popen(cmd, shell=True, cwd=working_dir)
    else:
        interpreter_binary = 'python'
        interpreter_binary_alt = 'python3'
        if platform.system() != 'Windows':
            interpreter_binary = 'python3'
            interpreter_binary_alt = 'python'
        print("execute in shell mode.")

        try:
            print('try', interpreter_binary)
            cmd_array = [interpreter_binary, script_name + '.py'] + cmd_argument
            s=subprocess.Popen(cmd_array, cwd=working_dir)
        except Exception as exc:
            print('try', interpreter_binary_alt)
            try:
                cmd_array = [interpreter_binary_alt, script_name + '.py'] + cmd_argument
                s=subprocess.Popen(cmd_array, cwd=working_dir)
            except Exception as exc:
                msg=str(exc)
                print("exeption:", msg)
                pass
