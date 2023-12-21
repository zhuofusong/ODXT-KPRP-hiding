"""
Plot the client, server and end-2-end search time
"""

import matplotlib.pyplot as plt
import pandas as pd


def generate_table(tables,logs,option = "ODXT-KPRP-hiding",check=False):
    df_2conj_changing_w1,df_2conj_changing_w1_cli,df_2conj_changing_w1_ser,df_2conj_changing_w1_comm,df_2conj_fixed_w1,df_2conj_fixed_w1_cli,df_2conj_fixed_w1_ser,df_2conj_fixed_w1_comm,df_6conj_changing_w1,df_6conj_changing_w1_cli,df_6conj_changing_w1_ser,df_6conj_changing_w1_comm,df_6conj_fixed_w1,df_6conj_fixed_w1_cli,df_6conj_fixed_w1_ser,df_6conj_fixed_w1_comm = tables

    logs_se,logs_cl = logs

    for ll in range(len(logs_se)):
        if logs_se[ll].startswith("Server search time for DB(w_1)=="):
            ll1 = ll
            break

    casecnt_2_ch = 0
    casecnt_2_fi = 0
    casecnt_6_ch = 0
    casecnt_6_fi = 0

    for ll in range(len(logs_cl)):
        if logs_cl[ll-1].startswith("############2 keyword search, changing DB(w_1)"):
            while not logs_cl[ll+casecnt_2_ch*4].startswith("############2 keyword search, fixed DB(w_1)"):
                w1_freq = logs_cl[ll+casecnt_2_ch*4].strip("\n").split(", ")[0]
                w1_freq = int(w1_freq.split("@")[1].lstrip("keyword"))
                if not check:
                    df_2conj_changing_w1_comm.loc[casecnt_2_ch, "Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq==df_2conj_changing_w1_comm.loc[casecnt_2_ch, "Upd(w1)"])
                df_2conj_changing_w1_comm.loc[casecnt_2_ch, option] = int(logs_cl[ll+casecnt_2_ch*4+1].strip("\n").split(" ")[-1])
                if not check:
                    df_2conj_changing_w1_cli.loc[casecnt_2_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_changing_w1_cli.loc[casecnt_2_ch,"Upd(w1)"])
                df_2conj_changing_w1_cli.loc[casecnt_2_ch,option] = float(logs_cl[ll+casecnt_2_ch*4+2].strip("\n").split("   ")[-1])
                if not check:
                    df_2conj_changing_w1.loc[casecnt_2_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_changing_w1.loc[casecnt_2_ch,"Upd(w1)"])
                df_2conj_changing_w1.loc[casecnt_2_ch,option] = float(logs_cl[ll+casecnt_2_ch*4+3].strip("\n").split(": ")[-1])

                assert(df_2conj_changing_w1_comm.loc[casecnt_2_ch,option] == int(logs_se[ll1-1].strip("\n").split(" ")[1]))
                if not check:
                    df_2conj_changing_w1_ser.loc[casecnt_2_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_changing_w1_ser.loc[casecnt_2_ch,"Upd(w1)"])
                df_2conj_changing_w1_ser.loc[casecnt_2_ch,option] = float(logs_se[ll1].strip("\n").split(": ")[-1])
                ll1 += 2

                casecnt_2_ch += 1
        elif logs_cl[ll-1].startswith("############2 keyword search, fixed DB(w_1)"):
            while not logs_cl[ll+casecnt_2_fi*4].startswith("############6 keyword search, changing DB(w_1)"):
                w1_freq = logs_cl[ll+casecnt_2_fi*4].strip("\n").split(", ")[1]
                w1_freq = int(w1_freq.split("@")[1].lstrip("keyword"))
                if not check:
                    df_2conj_fixed_w1_comm.loc[casecnt_2_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_fixed_w1_comm.loc[casecnt_2_fi,"Upd(w2)"])
                df_2conj_fixed_w1_comm.loc[casecnt_2_fi,option] = int(logs_cl[ll+casecnt_2_fi*4+1].strip("\n").split(" ")[-1])
                if not check:
                    df_2conj_fixed_w1_cli.loc[casecnt_2_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_fixed_w1_cli.loc[casecnt_2_fi,"Upd(w2)"])
                df_2conj_fixed_w1_cli.loc[casecnt_2_fi,option] = float(logs_cl[ll+casecnt_2_fi*4+2].strip("\n").split("   ")[-1])
                if not check:
                    df_2conj_fixed_w1.loc[casecnt_2_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_fixed_w1.loc[casecnt_2_fi,"Upd(w2)"])
                df_2conj_fixed_w1.loc[casecnt_2_fi,option] = float(logs_cl[ll+casecnt_2_fi*4+3].strip("\n").split(": ")[-1])

                assert(df_2conj_fixed_w1_comm.loc[casecnt_2_fi,option] == int(logs_se[ll1-1].strip("\n").split(" ")[1]))
                if not check:
                    df_2conj_fixed_w1_ser.loc[casecnt_2_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_2conj_fixed_w1_ser.loc[casecnt_2_fi,"Upd(w2)"])
                df_2conj_fixed_w1_ser.loc[casecnt_2_fi,option] = float(logs_se[ll1].strip("\n").split(": ")[-1])
                ll1 += 2

                casecnt_2_fi += 1

        elif logs_cl[ll-1].startswith("############6 keyword search, changing DB(w_1)"):
            while not logs_cl[ll+casecnt_6_ch*4].startswith("############6 keyword search, fixed DB(w_1)"):
                w1_freq = logs_cl[ll+casecnt_6_ch*4].strip("\n").split(", ")[0]
                w1_freq = int(w1_freq.split("@")[1].lstrip("keyword"))
                if not check:
                    df_6conj_changing_w1_comm.loc[casecnt_6_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_changing_w1_comm.loc[casecnt_6_ch,"Upd(w1)"])
                df_6conj_changing_w1_comm.loc[casecnt_6_ch,option] = int(logs_cl[ll+casecnt_6_ch*4+1].strip("\n").split(" ")[-1])
                if not check:
                    df_6conj_changing_w1_cli.loc[casecnt_6_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_changing_w1_cli.loc[casecnt_6_ch,"Upd(w1)"])
                df_6conj_changing_w1_cli.loc[casecnt_6_ch,option] = float(logs_cl[ll+casecnt_6_ch*4+2].strip("\n").split("   ")[-1])
                if not check:
                    df_6conj_changing_w1.loc[casecnt_6_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_changing_w1.loc[casecnt_6_ch,"Upd(w1)"])
                df_6conj_changing_w1.loc[casecnt_6_ch,option] = float(logs_cl[ll+casecnt_6_ch*4+3].strip("\n").split(": ")[-1])

                assert(df_6conj_changing_w1_comm.loc[casecnt_6_ch,option] == int(logs_se[ll1-1].strip("\n").split(" ")[1]))
                if not check:
                    df_6conj_changing_w1_ser.loc[casecnt_6_ch,"Upd(w1)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_changing_w1_ser.loc[casecnt_6_ch,"Upd(w1)"])
                df_6conj_changing_w1_ser.loc[casecnt_6_ch,option] = float(logs_se[ll1].strip("\n").split(": ")[-1])
                ll1 += 2

                casecnt_6_ch += 1

        elif logs_cl[ll-1].startswith("############6 keyword search, fixed DB(w_1)"):
            while ll+casecnt_6_fi*4 < len(logs_cl):
                w1_freq = logs_cl[ll+casecnt_6_fi*4].strip("\n").split(", ")[1]
                w1_freq = int(w1_freq.split("@")[1].lstrip("keyword"))
                if not check:
                    df_6conj_fixed_w1_comm.loc[casecnt_6_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_fixed_w1_comm.loc[casecnt_6_fi,"Upd(w2)"])
                df_6conj_fixed_w1_comm.loc[casecnt_6_fi,option] = int(logs_cl[ll+casecnt_6_fi*4+1].strip("\n").split(" ")[-1])
                if not check:
                    df_6conj_fixed_w1_cli.loc[casecnt_6_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_fixed_w1_cli.loc[casecnt_6_fi,"Upd(w2)"])
                df_6conj_fixed_w1_cli.loc[casecnt_6_fi,option] = float(logs_cl[ll+casecnt_6_fi*4+2].strip("\n").split("   ")[-1])
                if not check:
                    df_6conj_fixed_w1.loc[casecnt_6_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_fixed_w1.loc[casecnt_6_fi,"Upd(w2)"])
                df_6conj_fixed_w1.loc[casecnt_6_fi,option] = float(logs_cl[ll+casecnt_6_fi*4+3].strip("\n").split(": ")[-1])

                assert(df_6conj_fixed_w1_comm.loc[casecnt_6_fi,option] == int(logs_se[ll1-1].strip("\n").split(" ")[1]))
                if not check:
                    df_6conj_fixed_w1_ser.loc[casecnt_6_fi,"Upd(w2)"] = w1_freq
                else:
                    assert(w1_freq == df_6conj_fixed_w1_ser.loc[casecnt_6_fi,"Upd(w2)"])
                df_6conj_fixed_w1_ser.loc[casecnt_6_fi,option] = float(logs_se[ll1].strip("\n").split(": ")[-1])
                ll1 += 2

                casecnt_6_fi += 1
        
    # print(df_2conj_changing_w1.head())
    # print(df_2conj_changing_w1_cli.head())
    # print(df_2conj_changing_w1_ser.head())
    # print(df_2conj_changing_w1_comm.head())

    # print(df_2conj_fixed_w1.head())
    # print(df_2conj_fixed_w1_cli.head())
    # print(df_2conj_fixed_w1_ser.head())
    # print(df_2conj_fixed_w1_comm.head())

    # print(df_6conj_changing_w1.head())
    # print(df_6conj_changing_w1_cli.head())
    # print(df_6conj_changing_w1_ser.head())
    # print(df_6conj_changing_w1_comm.head())

    # print(df_6conj_fixed_w1.head())
    # print(df_6conj_fixed_w1_cli.head())
    # print(df_6conj_fixed_w1_ser.head())
    # print(df_6conj_fixed_w1_comm.head())

    return(df_2conj_changing_w1,df_2conj_changing_w1_cli,df_2conj_changing_w1_ser,df_2conj_changing_w1_comm,df_2conj_fixed_w1,df_2conj_fixed_w1_cli,df_2conj_fixed_w1_ser,df_2conj_fixed_w1_comm,df_6conj_changing_w1,df_6conj_changing_w1_cli,df_6conj_changing_w1_ser,df_6conj_changing_w1_comm,df_6conj_fixed_w1,df_6conj_fixed_w1_cli,df_6conj_fixed_w1_ser,df_6conj_fixed_w1_comm)



with open("test/result_client.log","r") as f:
    logs_cl = f.readlines()

with open("test/result_server.log","r") as f:
    logs_se = f.readlines()
logs_se = [kk for kk in logs_se if not kk.startswith("timed out")]

with open("test/result_client_odxt.log","r") as f:
    logs_cl_odxt = f.readlines()

with open("test/result_server_odxt.log","r") as f:
    logs_se_odxt = f.readlines()
logs_se_odxt = [kk for kk in logs_se_odxt if not kk.startswith("timed out")]

df_2conj_changing_w1 = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_2conj_changing_w1_cli = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_2conj_changing_w1_ser = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_2conj_changing_w1_comm = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])

df_2conj_fixed_w1 = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_2conj_fixed_w1_cli = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_2conj_fixed_w1_ser = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_2conj_fixed_w1_comm = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])

df_6conj_changing_w1 = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_6conj_changing_w1_cli = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_6conj_changing_w1_ser = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])
df_6conj_changing_w1_comm = pd.DataFrame( columns = ["Upd(w1)","ODXT","ODXT-KPRP-hiding"])

df_6conj_fixed_w1 = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_6conj_fixed_w1_cli = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_6conj_fixed_w1_ser = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])
df_6conj_fixed_w1_comm = pd.DataFrame( columns = ["Upd(w2)","ODXT","ODXT-KPRP-hiding"])

tables = (df_2conj_changing_w1,df_2conj_changing_w1_cli,df_2conj_changing_w1_ser,df_2conj_changing_w1_comm,df_2conj_fixed_w1,df_2conj_fixed_w1_cli,df_2conj_fixed_w1_ser,df_2conj_fixed_w1_comm,df_6conj_changing_w1,df_6conj_changing_w1_cli,df_6conj_changing_w1_ser,df_6conj_changing_w1_comm,df_6conj_fixed_w1,df_6conj_fixed_w1_cli,df_6conj_fixed_w1_ser,df_6conj_fixed_w1_comm)
tables = generate_table(tables,logs = (logs_se,logs_cl),option = "ODXT-KPRP-hiding",check=False)

tables = generate_table(tables,logs = (logs_se_odxt,logs_cl_odxt),option = "ODXT",check=True)

# for kk in tables:
#     print(kk)

df_2conj_changing_w1,df_2conj_changing_w1_cli,df_2conj_changing_w1_ser,df_2conj_changing_w1_comm,df_2conj_fixed_w1,df_2conj_fixed_w1_cli,df_2conj_fixed_w1_ser,df_2conj_fixed_w1_comm,df_6conj_changing_w1,df_6conj_changing_w1_cli,df_6conj_changing_w1_ser,df_6conj_changing_w1_comm,df_6conj_fixed_w1,df_6conj_fixed_w1_cli,df_6conj_fixed_w1_ser,df_6conj_fixed_w1_comm = tables

# plot 2-conj
def gen_2con_fig():
    fig, axs = plt.subplot_mosaic([['2-keyword conjunctive cli: changing Upd(w1)','2-keyword conjunctive cli: changing Upd(w2)'],['2-keyword conjunctive ser: changing Upd(w1)','2-keyword conjunctive ser: changing Upd(w2)'],['2-keyword conjunctive tot: changing Upd(w1)','2-keyword conjunctive tot: changing Upd(w2)'],['2-keyword conjunctive comm: changing Upd(w1)','2-keyword conjunctive comm: changing Upd(w2)']], layout='constrained')

    ax = axs['2-keyword conjunctive cli: changing Upd(w1)']
    ax.loglog(df_2conj_changing_w1_cli["Upd(w1)"],df_2conj_changing_w1_cli['ODXT-KPRP-hiding'])
    ax.loglog(df_2conj_changing_w1_cli["Upd(w1)"],df_2conj_changing_w1_cli['ODXT'])
    ax.set_ylabel("Client computation time (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive cli: changing Upd(w2)']
    ax.plot(df_2conj_fixed_w1_cli["Upd(w2)"],df_2conj_fixed_w1_cli['ODXT-KPRP-hiding'])
    ax.plot(df_2conj_fixed_w1_cli["Upd(w2)"],df_2conj_fixed_w1_cli['ODXT'])
    ax.set_ylabel("Client computation time (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.02)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive ser: changing Upd(w1)']
    ax.loglog(df_2conj_changing_w1_ser["Upd(w1)"],df_2conj_changing_w1_ser['ODXT-KPRP-hiding'])
    ax.loglog(df_2conj_changing_w1_ser["Upd(w1)"],df_2conj_changing_w1_ser['ODXT'])
    ax.set_ylabel("Server computation time (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive ser: changing Upd(w2)']
    ax.plot(df_2conj_fixed_w1_ser["Upd(w2)"],df_2conj_fixed_w1_ser['ODXT-KPRP-hiding'])
    ax.plot(df_2conj_fixed_w1_ser["Upd(w2)"],df_2conj_fixed_w1_ser['ODXT'])
    ax.set_ylabel("Server computation time (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.03)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive tot: changing Upd(w1)']
    ax.loglog(df_2conj_changing_w1["Upd(w1)"],df_2conj_changing_w1['ODXT-KPRP-hiding'])
    ax.loglog(df_2conj_changing_w1["Upd(w1)"],df_2conj_changing_w1['ODXT'])
    ax.set_ylabel("Total latency (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive tot: changing Upd(w2)']
    ax.plot(df_2conj_fixed_w1["Upd(w2)"],df_2conj_fixed_w1['ODXT-KPRP-hiding'])
    ax.plot(df_2conj_fixed_w1["Upd(w2)"],df_2conj_fixed_w1['ODXT'])
    ax.set_ylabel("Total latency (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.05)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive comm: changing Upd(w1)']
    ax.loglog(df_2conj_changing_w1_comm["Upd(w1)"],df_2conj_changing_w1_comm['ODXT-KPRP-hiding']/1024)
    ax.loglog(df_2conj_changing_w1_comm["Upd(w1)"],df_2conj_changing_w1_comm['ODXT']/1024)
    ax.set_ylabel("Communication overhead (KB)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['2-keyword conjunctive comm: changing Upd(w2)']
    ax.plot(df_2conj_fixed_w1_comm["Upd(w2)"],df_2conj_fixed_w1_comm['ODXT-KPRP-hiding']/1024)
    ax.plot(df_2conj_fixed_w1_comm["Upd(w2)"],df_2conj_fixed_w1_comm['ODXT']/1024)
    ax.set_ylabel("Communication overhead (KB)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=3)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])
    plt.show()


# plot 6-conj
def gen_6con_fig():
    fig, axs = plt.subplot_mosaic([['6-keyword conjunctive cli: changing Upd(w1)','6-keyword conjunctive cli: changing Upd(w2)'],['6-keyword conjunctive ser: changing Upd(w1)','6-keyword conjunctive ser: changing Upd(w2)'],['6-keyword conjunctive tot: changing Upd(w1)','6-keyword conjunctive tot: changing Upd(w2)'],['6-keyword conjunctive comm: changing Upd(w1)','6-keyword conjunctive comm: changing Upd(w2)']], layout='constrained')

    ax = axs['6-keyword conjunctive cli: changing Upd(w1)']
    ax.loglog(df_6conj_changing_w1_cli["Upd(w1)"],df_6conj_changing_w1_cli['ODXT-KPRP-hiding'])
    ax.loglog(df_6conj_changing_w1_cli["Upd(w1)"],df_6conj_changing_w1_cli['ODXT'])
    ax.set_ylabel("Client computation time (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive cli: changing Upd(w2)']
    ax.plot(df_6conj_fixed_w1_cli["Upd(w2)"],df_6conj_fixed_w1_cli['ODXT-KPRP-hiding'])
    ax.plot(df_6conj_fixed_w1_cli["Upd(w2)"],df_6conj_fixed_w1_cli['ODXT'])
    ax.set_ylabel("Client computation time (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.08)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive ser: changing Upd(w1)']
    ax.loglog(df_6conj_changing_w1_ser["Upd(w1)"],df_6conj_changing_w1_ser['ODXT-KPRP-hiding'])
    ax.loglog(df_6conj_changing_w1_ser["Upd(w1)"],df_6conj_changing_w1_ser['ODXT'])
    ax.set_ylabel("Server computation time (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive ser: changing Upd(w2)']
    ax.plot(df_6conj_fixed_w1_ser["Upd(w2)"],df_6conj_fixed_w1_ser['ODXT-KPRP-hiding'])
    ax.plot(df_6conj_fixed_w1_ser["Upd(w2)"],df_6conj_fixed_w1_ser['ODXT'])
    ax.set_ylabel("Server computation time (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.14)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive tot: changing Upd(w1)']
    ax.loglog(df_6conj_changing_w1["Upd(w1)"],df_6conj_changing_w1['ODXT-KPRP-hiding'])
    ax.loglog(df_6conj_changing_w1["Upd(w1)"],df_6conj_changing_w1['ODXT'])
    ax.set_ylabel("Total latency (s)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive tot: changing Upd(w2)']
    ax.plot(df_6conj_fixed_w1["Upd(w2)"],df_6conj_fixed_w1['ODXT-KPRP-hiding'])
    ax.plot(df_6conj_fixed_w1["Upd(w2)"],df_6conj_fixed_w1['ODXT'])
    ax.set_ylabel("Total latency (s)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=0.25)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive comm: changing Upd(w1)']
    ax.loglog(df_6conj_changing_w1_comm["Upd(w1)"],df_6conj_changing_w1_comm['ODXT-KPRP-hiding']/1024)
    ax.loglog(df_6conj_changing_w1_comm["Upd(w1)"],df_6conj_changing_w1_comm['ODXT']/1024)
    ax.set_ylabel("Communication overhead (KB)")
    ax.set_xlabel("(a): Upd(w1)")
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    ax = axs['6-keyword conjunctive comm: changing Upd(w2)']
    ax.plot(df_6conj_fixed_w1_comm["Upd(w2)"],df_6conj_fixed_w1_comm['ODXT-KPRP-hiding']/1024)
    ax.plot(df_6conj_fixed_w1_comm["Upd(w2)"],df_6conj_fixed_w1_comm['ODXT']/1024)
    ax.set_ylabel("Communication overhead (KB)")
    ax.set_xlabel("(b): Upd(w2)")
    ax.set_ylim(bottom=0,top=7)
    ax.legend(['ODXT-KPRP-hiding','ODXT'])

    plt.show()

gen_2con_fig()

gen_6con_fig()