#!/usr/bin/env python3

import time
import os
import json
from jinja2 import Environment, BaseLoader, exceptions
from pprintjson import pprintjson
from colorama import Fore, Style


def main():
    ORG_, ENV_, APP_, cnf, tgt_proj_dir = set_vars()
    do_generate(ORG_, ENV_ , APP_ , cnf, tgt_proj_dir)


def print_warn(msg):
    print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")


def print_error(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")


def print_success(msg):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")


def set_vars():
    try:
        product_dir = os.path.join(__file__, "..", "..", "..", "..", "..")
        product_dir = os.path.abspath(product_dir)
        # override with another base dir if we need to run against another proj
        ORG_ = os.getenv("ORG")
        APP_ = os.getenv("APP")
        ENV_ = os.getenv("ENV")

        tgt_proj_dir = os.getenv("TGT_PROJ_DIR",product_dir)
        json_cnf_file = os.getenv("JSON_CNF_FILE", default=f"{tgt_proj_dir}/cnf/env/{ORG_}/{APP_}/{ENV_}.env.json")
        print(f'''
        product_dir: {product_dir}
        tgt_proj_dir: {tgt_proj_dir}
        json_cnf_file: {json_cnf_file}
        ''')

        print(f"tpl_gen.py ::: using config json file: {json_cnf_file}")
        time.sleep(1)

        with open(json_cnf_file, encoding="utf-8") as json_cnf_file:
            cnf = json.load(json_cnf_file)

        pprintjson(cnf)

    except IndexError as error:
        raise Exception("ERROR in set_vars: ", str(error)) from error

    return ORG_, ENV_, APP_, cnf, tgt_proj_dir


def do_generate(ORG_, ENV_, APP_, cnf, tgt_proj_dir):
    tpl_dir = os.getenv("TPL_DIR", default=f"{tgt_proj_dir}/src/tpl/",)

    for pathname in tpl_dir:
        for subdir, _dirs, files in os.walk(pathname):
            for file in files:
                current_file_path = os.path.join(subdir, file)
                if current_file_path.endswith(".tpl"):
                    try:
                        with open(current_file_path, "r", encoding="utf-8") as current_file:
                            str_tpl = current_file.read()
                            obj_tpl = Environment(loader=BaseLoader) \
                                .from_string(str_tpl)
                            args = os.environ.copy()
                            args.update(cnf["env"])
                            rendered = obj_tpl.render(args)

                            tgt_file_path = os.getenv("TGT_FILE_PATH", default=current_file_path.replace("/src/tpl", "", 1) \
                                .replace(".tpl", "") \
                                .replace(r"%env%", ENV_) \
                                .replace(r"%org%", ORG_) \
                                .replace(r"%app%", APP_)
                            )
                            print(tgt_file_path)


                            if not os.path.exists(os.path.dirname(tgt_file_path)):
                                os.makedirs(os.path.dirname(tgt_file_path))

                            with open(tgt_file_path, "w", encoding="utf-8") as tgt_file:
                                tgt_file.write(rendered + os.linesep)
                                msg = f"File \"{tgt_file_path}\" rendered with success."
                                print_success(msg)

                    except exceptions.UndefinedError as error:
                        msg = "WARNING: Missing variable in json config in file: " + \
                            f"\"{current_file_path}\" - {error}"
                        print_warn(msg)

                    except Exception as error:
                        print_error(f"RENDERING EXCEPTION: \n{error}")
                        raise error

    print("STOP generating templates")


if __name__ == "__main__":
    main()
