import psutil
import ctypes
import win32process
import win32api
import win32con


# 获取目标进程ID
def get_process_id_by_name(process_name):
    # 获取所有运行中的进程
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None


# 读取内存函数
def read_memory(pid, address, size=4):
    # 获取目标进程的句柄
    process_handle = win32api.OpenProcess(win32con.PROCESS_VM_READ, False, pid)

    # 读取指定地址的内存
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_ulong(0)
    result = win32process.ReadProcessMemory(process_handle, address, buffer, size, ctypes.byref(bytes_read))

    # 转换为需要的数据类型（假设是整型）
    if result:
        return ctypes.c_uint.from_buffer(buffer).value
    else:
        print(f"Failed to read memory at address {hex(address)}")
        return None


# 示例：读取游戏进程中的某个内存地址
def main():
    # 设置目标进程名称
    process_name = "game.exe"  # 修改为你游戏的进程名
    pid = get_process_id_by_name(process_name)

    if pid is None:
        print(f"Could not find process {process_name}")
        return

    print(f"Found process {process_name} with PID {pid}")

    # 假设我们知道某个内存地址（你需要通过调试工具获取该地址）
    address = 0x00A2B3C4  # 这是一个示例地址，真实地址需要通过分析得到

    # 读取该地址的4个字节的数据（例如角色的生命值）
    value = read_memory(pid, address, size=4)

    if value is not None:
        print(f"Memory value at {hex(address)}: {value}")


if __name__ == "__main__":
    main()
