#!/usr/bin/python3

import subprocess
import argparse

def check_partition():
    df_output = subprocess.check_output(["df", "/srv"]).decode("utf-8")
    usage_line = df_output.strip().split("\n")[1]
    usage_percent = int(usage_line.split()[4].replace("%", ""))
    return usage_percent

def extend_volume(vg_name, lv_name):
    subprocess.run(["lvextend", "-L", "+1G", f"/dev/{vg_name}/{lv_name}"])
    subprocess.run(["resize2fs", f"/dev/{vg_name}/{lv_name}"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extend Logical Volume if partition usage is above 99%.")
    parser.add_argument("--vg", help="Volume Group name", required=True)
    parser.add_argument("--lv", help="Logical Volume name", required=True)
    args = parser.parse_args()

    partition_usage = check_partition()
    if partition_usage >= 98:
        extend_volume(args.vg, args.lv)
        print("Logical Volume extended successfully.")
    else:
        print("Partition below 99%. No extension required.")
