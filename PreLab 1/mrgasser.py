
def ip_conversion(num):
    ip_list = num.split(".")
    print(ip_list)
    out_list = []
    for i in ip_list:
        val = int(i)
        bin_num = ""
        while val:
            bin_num + val%2
            val = val // 2
        out_list.append(bin_num)
    return out_list
        

if __name__ == '__main__':
    ip = input("Enter the desired IP address in dotted decimal form :")
    print(ip)
    output = ip_conversion(ip)