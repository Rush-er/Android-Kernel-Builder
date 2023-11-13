import os
import json
import argparse
import colorama

parser = argparse.ArgumentParser(description='Open kernel configuration.')
parser.add_argument('-w', '--write', action='store_true', default=False, help='Whether to write to file')
parser.add_argument('defconfig', type=argparse.FileType('r'))
args = parser.parse_args()

root = os.path.dirname(os.path.abspath(__file__))
configs_add = {}


def main():
    # Read Config configuration from file
    with open(os.path.join(root, "Config.json")) as f:
        configs_add = json.load(f)

    defconfig_content = args.defconfig.read()

    # Update existing entries
    configs = dict(
        line.split("=") for line in [config for config in defconfig_content.splitlines() if not config.startswith("#")])
    for k, v in configs_add.items():
        if k in configs:
            if configs[k] != v:
                print(f"{colorama.Fore.RED}[{k}={v}] reset to [{v}]{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.YELLOW}Duplicate [{k}={v}]{colorama.Style.RESET_ALL}")
        configs[k] = v

    new_defconfig_content = "\n".join(f"{k}={v}" for k, v in configs.items())
    if args.write:
        # Write updated configuration back to the source file
        origin_file = os.path.abspath(args.defconfig.name)
        with open(origin_file + ".bak", 'w') as bak_file:
            bak_file.write(defconfig_content)
        with open(args.defconfig.name, 'w') as config_file:
            config_file.write(new_defconfig_content)
        print(f"Updated configuration written to {args.defconfig.name}")
    else:
        print(new_defconfig_content)


if __name__ == "__main__":
    main()
