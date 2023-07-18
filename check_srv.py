#!/usr/bin/python3

import subprocess
import argparse
from datetime import datetime

def check_partition():
    df_output = subprocess.check_output(["df", "/srv"]).decode("utf-8")
    usage_line = df_output.strip().split("\n")[1]
    usage_percent = int(usage_line.split()[4].replace("%", ""))
    return usage_percent

def extend_volume(vg_name, lv_name):
    def run_cmmd(cmmd):
        proc = subprocess.Popen(cmmd, stdout=subprocess.PIPE, \
        stderr=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
        return [out.strip(), err.strip()]

    try:
        cmmd = ["lvextend", "-L", "+1G", f"/dev/{vg_name}/{lv_name}", "--resize"]
        res = run_cmmd(cmmd)
        if 'free space' in res[1].lower():
            return f'Insufficient free space in VG: {vg_name}'
        else:
            return f'Logical Volume extended successfully, {lv_name} with {check_partition()}%.'

    except subprocess.CalledProcessError as e:
        print(f"Except, an error extending Logical Volume: {e}")
        return(f"Except, an error extending Logical Volume: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extend Logical Volume if partition usage is above 98%.")
    parser.add_argument("--vg", help="Volume Group name", required=True)
    parser.add_argument("--lv", help="Logical Volume name", required=True)
    args = parser.parse_args()

    partition_usage = check_partition()
    if partition_usage >= 98:
        res = extend_volume(args.vg, args.lv)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {res}")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Partition {partition_usage}%, below of 98%. No extension required.")
