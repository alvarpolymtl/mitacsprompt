import psycopg2
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sn

def load_data(schema, table):
    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    data = pd.read_sql(sql_command, conn)
    return (data)

#Database connection with schema.public.Canada_2017_TechnologyTotals.TXT
conn = psycopg2.connect(host="XXXXXXXX",database="XXXXXX", user="XXXXXX", password="XXXXXXXX")
cursor = conn.cursor()
cursor.execute("SET search_path TO public")
data = load_data("public","\"Canada_2017_TechnologyTotals.TXT\"")

#We create a plot for PCS y DESKTOPS on Canada_2017_TechnologyTotals.TXT
fig, ax = plt.subplots()
ax.scatter(data['PCS'], data['DESKTOPS'])
ax.set_title('PCS VS DESKTOPS')
ax.set_xlabel('PCS')
ax.set_ylabel('DESKTOPS')
plt.savefig('.png')
plt.show()

#We create a histogram for PCS,DESKTOPS, LAPTOPS de Canada_2017_TechnologyTotals.TXT
pcs = data['PCS']
legend = ['PCS', 'DESKTOP','LAPTOPS']
desktops = data['DESKTOPS']
laptops = data['LAPTOPS']
plt.hist([pcs, desktops, laptops], color=['orange', 'green', 'red'],bins=30)
ax.set_title('PCS VS DESKTOPS')
plt.xlabel("Points")
plt.ylabel("Frequency")
plt.legend(legend)
plt.title('PCS vs Desktops vs Laptops Histogram')
plt.show()

#This part runs from 2016 to 2018 Canada_Year_TechnologyTotals.TXT
#We generate HeatMaps for the correlation matrix between PCS, desktops, laptops, etc.
# A bar plot is also shown to observe PCS centralization
for i in range(0,3):
    path_str = "\"Canada_{}_TechnologyTotals.TXT\"".format(str(2016+i))
    data = load_data("public",path_str)
    data['PCS'].value_counts().sort_index().plot.bar()
    plt.show()
    df = DataFrame(data, columns=['PCS', 'DESKTOPS', 'LAPTOPS','SERVERS', 'PRINTERS'])
    sn.heatmap(df.corr(), annot=True)
    plt.show()
suma_it_budget = []
suma_soft_budget = []

#Return Canada _ {} _ Hist {} _ ITSPEND from 2011 to 2015 and obtain its heat map for the data IT_BUDGET, HARDWARE_BUDGET, ETC
#We get the sum per year of IT and Software
for i in range(0,5):
    path_str = "\"Canada_{}_Hist{}_ITSPEND\"".format(str(2011+i),str(2011+i))
    data = load_data("public",path_str)
    suma_it_budget.append(np.sum(data['IT_BUDGET']))
    suma_soft_budget.append(np.sum(data['SOFTWARE_BUDGET']))
    df = DataFrame(data, columns=['IT_BUDGET', 'PC_BUDGET', 'HARDWARE_BUDGET','TERMINAL_BUDGET', 'PRINTER_BUDGET','SOFTWARE_BUDGET','OTHER_HARDWARE_BUDGET'])
    sn.heatmap(df.corr(), annot=True)
    plt.show()

#This bar plot allows you to observe the annual behavior of the IT_BUDGET budget against SOFT_BUDGET

labels = ['2010', '2012', '2013', '2014', '2015']
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, suma_it_budget, width, label='IT_Budget')
rects2 = ax.bar(x + width/2, suma_soft_budget, width, label='Soft_Budget')
ax.set_ylabel('Budget')
ax.set_title('Total Budget per year')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.title('IT_Budget vs Software_BUdget')

plt.show()

#We close PostgreSQL's connection
if(conn):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")



