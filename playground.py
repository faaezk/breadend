import pandas as pd
import numpy as np

data = ["1724,Sunday-July-10-2022-7:42-AM", "1707,Sunday-July-10-2022-8:18-AM", "1700,Sunday-July-10-2022-9:14-AM", "1721,Sunday-July-10-2022-9:52-AM", 
    "1710,Sunday-July-10-2022-12:22-PM", "1723,Sunday-July-10-2022-1:07-PM", "1712,Sunday-July-10-2022-1:55-PM", "1700,Monday-July-11-2022-12:28-PM",
    "1720,Monday-July-11-2022-1:19-PM",  "1736,Monday-July-11-2022-2:08-PM", "1750,Monday-July-11-2022-2:54-PM", "1736,Monday-July-11-2022-4:52-PM", 
    "1755,Tuesday-July-12-2022-9:51-AM", "1741,Tuesday-July-12-2022-2:05-PM", "1755,Tuesday-July-12-2022-2:54-PM","1771,Tuesday-July-12-2022-3:59-PM",
    "1768,Tuesday-July-12-2022-4:44-PM", "1755,Tuesday-July-12-2022-4:48-PM", "1772,Wednesday-July-13-2022-7:41-AM", "1757,Wednesday-July-13-2022-8:28-AM", 
    "1774,Wednesday-July-13-2022-9:20-AM", "1796,Wednesday-July-13-2022-12:08-PM" ,"1816,Wednesday-July-13-2022-12:41-PM", "1801,Wednesday-July-13-2022-1:18-PM", 
    "1800,Wednesday-July-13-2022-4:35-PM", "1785,Thursday-July-14-2022-12:11-PM", "1810,Thursday-July-14-2022-12:58-PM", "1824,Thursday-July-14-2022-3:17-PM", 
    "1840,Thursday-July-14-2022-4:00-PM", "1861,Friday-July-15-2022-5:33-AM", "1843,Friday-July-15-2022-6:06-AM", "1862,Friday-July-15-2022-6:40-AM", 
    "1880,Friday-July-15-2022-10:00-AM", "1864,Friday-July-15-2022-12:08-PM", "1848,Friday-July-15-2022-12:50-PM", "1868,Saturday-July-16-2022-1:58-PM", 
    "1852,Saturday-July-16-2022-2:39-PM", "1840,Saturday-July-16-2022-3:38-PM", "1827,Saturday-July-16-2022-4:27-PM", 
    "1847,Sunday-July-17-2022-6:52-AM",  "1865,Sunday-July-17-2022-12:17-PM", "1847,Sunday-July-17-2022-1:14-PM", "1831,Sunday-July-17-2022-1:50-PM", 
    "1846,Sunday-July-17-2022-3:28-PM", "1832,Sunday-July-17-2022-4:07-PM", "1852,Monday-July-18-2022-1:05-PM", "1834,Tuesday-July-19-2022-4:53-AM", 
    "1854,Tuesday-July-19-2022-5:39-AM", "1837,Tuesday-July-19-2022-12:14-PM", "1823,Tuesday-July-19-2022-1:08-PM", "1808,Tuesday-July-19-2022-3:50-PM", 
    "1825,Tuesday-July-19-2022-4:23-PM", "1846,Wednesday-July-20-2022-6:14-AM", "1831,Wednesday-July-20-2022-6:52-AM", "1814,Wednesday-July-20-2022-7:38-AM", 
    "1800,Wednesday-July-20-2022-8:19-AM", "1819,Wednesday-July-20-2022-11:52-AM", "1802,Wednesday-July-20-2022-12:45-PM", "1822,Thursday-July-21-2022-2:17-PM",
    "1835,Thursday-July-21-2022-3:10-PM", "1817,Friday-July-22-2022-3:40-AM", "1838,Friday-July-22-2022-4:10-AM", "1822,Friday-July-22-2022-1:51-PM", 
    "1839,Friday-July-22-2022-2:25-PM", "1852,Friday-July-22-2022-2:53-PM", "1874,Saturday-July-23-2022-4:45-AM", "1892,Saturday-July-23-2022-5:40-AM", 
    "1875,Saturday-July-23-2022-6:39-AM", "1861,Saturday-July-23-2022-12:58-PM", "1881,Saturday-July-23-2022-1:54-PM", "1863,Saturday-July-23-2022-2:35-PM",
    "1850,Saturday-July-23-2022-3:48-PM", "1864,Saturday-July-23-2022-4:28-PM", "1886,Sunday-July-24-2022-5:39-AM", "1910,Sunday-July-24-2022-6:11-AM", 
    "1900,Sunday-July-24-2022-7:10-AM", "1884,Monday-July-25-2022-2:10-PM", "1910,Monday-July-25-2022-2:48-PM", "1900,Monday-July-25-2022-3:26-PM", 
    "1882,Monday-July-25-2022-4:02-PM", "1899,Tuesday-July-26-2022-12:28-PM", "1921,Tuesday-July-26-2022-1:50-PM", "1902,Tuesday-July-26-2022-2:24-PM", 
    "1914,Wednesday-July-27-2022-1:43-PM", "1928,Wednesday-July-27-2022-2:27-PM", "1910,Thursday-July-28-2022-4:40-AM", "1926,Thursday-July-28-2022-5:39-AM", 
    "1905,Thursday-July-28-2022-9:45-AM", "1924,Thursday-July-28-2022-2:33-PM", "1910,Thursday-July-28-2022-4:01-PM", "1900,Friday-July-29-2022-12:06-PM", 
    "1914,Friday-July-29-2022-1:47-PM", "1900,Friday-July-29-2022-2:23-PM", "1919,Saturday-July-30-2022-6:14-AM", "1940,Saturday-July-30-2022-7:03-AM", 
    "1917,Saturday-July-30-2022-7:36-AM", "1900,Saturday-July-30-2022-8:00-AM"]

months = {"January" : 1, "February" : 2, "March" : 3, 
        "April" : 4, "May" : 5, "June" : 6,
        "July" : 7, "August" : 8, "September" : 9, 
        "October" : 10, "November" : 11, "December" : 12}

rows_list = []
for i in range(len(data)):
        temp = data[i].split(',')
        ts = temp[1].split('-')
        dict1 = {'x' : i + 1, 'y' : temp[0], 'dates' : f"{ts[2]}/{months[ts[1]]}"}
        dict1.update()
        rows_list.append(dict1)

df = pd.DataFrame(rows_list)

yint = max(df['y'])
print(yint)