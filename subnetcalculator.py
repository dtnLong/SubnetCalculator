def getIPclass(ip_str):
    first_byte = int(ip_str.split(".")[0])
    if first_byte < 128:
        return ['255', 24]
    elif first_byte < 192:
        return ['255.255', 16]
    else:
        return ['255.255.255', 8]


def calculate_borrow_bits(host, host_len):
    for i in range(1, host_len + 1, 1):
        if pow(2, i) >= host:
            borrowed = ''
            for bit in range(0, host_len - i, 1):
                borrowed = borrowed + '1'
            borrowed_bit_whole_count = len(borrowed) // 8
            host_bit_whole_count = (host_len - len(borrowed)) // 8
            non_whole_borrowed_bit = borrowed[-1 * len(borrowed) + borrowed_bit_whole_count * 8:]
            print("Borrowed bit whole count: ", borrowed_bit_whole_count)
            print("Host bit whole count: ", host_bit_whole_count)
            print("Borrowed bit non-whole: ", non_whole_borrowed_bit)
            return [borrowed_bit_whole_count, host_bit_whole_count, non_whole_borrowed_bit]


def calculate_borrow_dec(borrowed_bit_whole_count, host_bit_whole_count, non_whole_borrowed_bit):
    borrowed_str = ''
    for i in range(0, borrowed_bit_whole_count):
        borrowed_str = borrowed_str + ".255"
    borrowed_str = borrowed_str + "." + str(convert(non_whole_borrowed_bit))
    for i in range(0, host_bit_whole_count):
        borrowed_str = borrowed_str + ".0"
    return borrowed_str
    # borrowed_whole_oct = len(borrowed_bit) // 8
    # borrowed_non_whole_len = len(borrowed_bit) % 8
    # if (borrowed_non_whole_len == 1):
    #     borrowed_non_whole_bit = '1'
    # else:
    #     borrowed_non_whole_bit = borrowed_bit[-1 * borrowed_non_whole_len:-1]
    # print("Borrowed_whole: ", borrowed_whole_oct)
    # print("Borrowed non whole len: ", borrowed_non_whole_len)
    # print("Borrowed bit: ", borrowed_bit)
    # print("Host bit whole: ", borrowed_bit_whole)
    # for i in range(borrowed_whole_oct):
    #     borrowed_str = borrowed_str + '255.'
    # borrowed_str = borrowed_str + convert(borrowed_non_whole_bit)
    # for i in range(borrowed_bit_whole):
    #     borrowed_str = borrowed_str + '.0'


def convert(bin_str):
    bin_str_len = len(bin_str)
    dec_result = 0
    for i in range(0, bin_str_len, 1):
        dec_result = dec_result + (int(bin_str[i]) * pow(2, 7 - i))
    return str(dec_result)


def AND(num1, num2):
    num1 = str(bin(num1)[2:])
    num2 = str(bin(num2)[2:])
    result = ""
    for i in range(8 - len(num1)):
        num1 = '0' + num1
    for i in range(len(num1)):
        if num1[i] == '1' and num2[i] == '1':
            result = result + '1'
        else:
            result = result + '0'
    result = str(int(result, 2))
    return result


def calculate_network_address(ip_address, subnet_mask):
    network_address = ip_address.split(".")[0]
    ip_address_loc = 0
    subnet_mask_loc = 0
    for index, octet in enumerate(subnet_mask.split(".")):
        if index == 0:
            continue
        if octet == "0":
            network_address = network_address + "." + "0"
        elif subnet_mask[index] != "255":
            ip_address_loc = int(ip_address.split(".")[index])
            subnet_mask_loc = int(octet)
            network_address = network_address + "." + AND(ip_address_loc, subnet_mask_loc)
        else:
            network_address = network_address + "." + ip_address.split(".")[index]
    return network_address


def calculate_address(ip_address, subnet_mask, subnet_host_list):
    base_network_address = calculate_network_address(ip_address, subnet_mask)
    print("Network address: ", base_network_address)
    base_subnet_multiplier = 256 - int(subnet_mask.split(".")[3])
    subnet_multiplier_current = int(base_network_address.split(".")[3]) + base_subnet_multiplier
    host_address = int(base_network_address.split(".")[3])
    network_address = base_network_address.split(".")[0] + "." + base_network_address.split(".")[1] + "." + base_network_address.split(".")[2] + "."
    for index, host in enumerate(subnet_host_list):
        print("Network address of subnet", index + 1, ": ", network_address + str(host_address))
        host_address = host_address + 1
        for i in range(host - 2):
            print("Subnet ", index + 1, "host ", i + 1, ": ", network_address + str(host_address))
            host_address = host_address + 1
        print("Subnet ", index + 1, "broadcast address: ", network_address + str(host_address))
        host_address = host_address + (subnet_multiplier_current - host_address)
        subnet_multiplier_current = subnet_multiplier_current + base_subnet_multiplier
        print()


def main():
    ip_str = input("Enter IP address: ")
    subnets = int(input("Enter needed subnets: "))
    subnet_host_list = []
    max_host = 0
    for i in range(1, subnets + 1, 1):
        host = int(input("Enter needed host for subnet " + str(i) + ": ")) + 2
        subnet_host_list.append(host)
        if host > max_host:
            max_host = host
    print()
    ip_class = getIPclass(ip_str)
    borrow_bits_info = calculate_borrow_bits(max_host, ip_class[1])
    print()
    if borrow_bits_info[2] == "":
        print("Cannot create subnets")
    else:
        subnet_mask = ip_class[0] + calculate_borrow_dec(borrow_bits_info[0], borrow_bits_info[1], borrow_bits_info[2])
        print("Subnet: ", subnet_mask)
        calculate_address(ip_str, subnet_mask, subnet_host_list)


if __name__ == '__main__':
    main()
