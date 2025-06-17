from helpers.custom_thread import TomChienXuOJThread
from handlers.violation import safely_get_violations

def main():
  bien_so_xe = input("Nhập biển số xe: ")
  loai_xe = input("Nhập loại xe: ")
  
  thread = TomChienXuOJThread(target=safely_get_violations, args=(bien_so_xe, loai_xe))
  thread.start()
  result = thread.join(timeout=10)

  if thread.is_alive():
    thread.join()

  # TomChienXu Note: Timeout
  if result is None:
    print("Timed out. (Network error, connection issue, or CSGT.vn is down/inaccessible)")

  # TomChienXu Note: Max Captcha Attempts reached
  if result.get("violations") is None:
    print("Max Captcha attempts reached. Please try again!")
  else:
    violations = result.get("violations")
    
    if len(violations) == 0:
      print("Không có vi phạm nào.")
    else:
      for index, violation in enumerate(violations):
        print("INDEX #" + str(index))
        
        for key in violation:
            print (key, ":", violation[key])

if __name__ == "__main__":
  main()
