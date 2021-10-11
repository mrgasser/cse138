import re

bin_check = False

def dec_to_bin_conversion(num):
    ip_list = num.split(".")
    out_list = []
    for i in ip_list:
        val = int(i)
        bin_num = ""
        while val:
            bin_num = str(val%2) + bin_num
            val = val // 2
        while len(bin_num) != 8:
            bin_num = "0" + bin_num
        out_list.append(bin_num)
    return out_list

def bin_to_dec_conversion(num):
    l = num.split()
    out_list = []
    for i in l:
        out_list.append(int(i, 2))
    return out_list   

def check_input(str):
    x = re.search("[a-zA-Z]", str)
    if x:
        print("invalid input")
        exit()
    else:
        y = re.search("[0-9]\.", str)
        if y:
            print("converting to BIN")
            output = dec_to_bin_conversion(str)
            return output, 0
        else:
            bin_check = True
            print("converting to decimal")
            output = bin_to_dec_conversion(str)
            return output, 1

def format_output(output, check):
    out_str = ""
    if check:
        for i in range(0, len(output)):
            out_str = out_str + str(output[i])
            if i + 1 != len(output):
                out_str = out_str + "."
    else:
        for i in range(0, len(output)):
            out_str = out_str + str(output[i])
            if i + 1 != len(output):
                out_str = out_str + " "
    print(out_str)

if __name__ == '__main__':
    ip = input("Enter the desired IP address in dotted decimal form or binary form:")
    #print(ip)
    out, check = check_input(ip)
    format_output(out, check)