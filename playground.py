import classyval_online
import valorant_online
import classier_online
import time

start_time = time.time()
valorant_online.get_all_data()
valorant_online.everything()
print("Process finished --- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
classyval_online.get_all_data()
classyval_online.main()
print("Process finished --- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
classier_online.loadData()
classier_online.main()
print("Process finished --- %s seconds ---" % (time.time() - start_time))