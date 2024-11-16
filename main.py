import pandas as pd


def sorter(frame_list):
    """Simple function for sorting rows of our DataFrame, and changing index's"""
    sorted_data = sorted(frame_list, key=lambda x: float(x['Total']), reverse=True)
    position=1
    for record in sorted_data:
        record.update({"Column1": str(position)})
        position+=1
    return sorted_data

def csv_parser(leaderboard_csv, new_data_csv):
    """Main parser"""
    leaderboard_frame = pd.read_csv(leaderboard_csv) # Read our main file
    empty_fields = []
    for index, row in leaderboard_frame.iterrows():
        if type(row.to_dict()['Column2']) is float:
            empty_fields.append(index)  # find tables separator
    lst = leaderboard_frame.columns.to_list()
    last_r_column = None #Find the last R-column
    for index, element in enumerate(lst):
        if element == 'Total':
            number = (lst[index-1])
            last_r_column = int(''.join(number[1:]))
    leaderboard_frame.insert((last_r_column+2), f"R{last_r_column+1}", pd.NA) #Insert new column for future
    work_frame = leaderboard_frame.iloc[(int(empty_fields[-1]) + 2):] # Our work frame
    date_frame = pd.read_csv(new_data_csv) # our new data
    datas = []
    for index, row in date_frame.iterrows():
        datas.append(row.to_dict())
    last_row_index = None # This point for new record index
    column_for_fill= None # R-column for fill
    processed_records = []
    for record in datas:
        for index, row in work_frame.iterrows():
            if not last_row_index:
                if pd.isna(row.to_dict()['Column1']):
                    last_row_index = index - 1
            if row.to_dict()['Column2'] in record['name']: #create new record in column
                for column, value in row.to_dict().items():
                    if pd.isna(value):
                        if float(row.to_dict()['Total'])+record['score'] <150.0:
                            summ = float(row.to_dict()['Total'])+record['score']
                            work_frame.at[index, column] = record['score']
                            work_frame.at[index, "Total"] = round(summ, 2)
                            work_frame.at[index, "Spent"] = round((150.0 - summ),2)
                            work_frame.at[index, "Percent"] = f"{round(((150.0 - summ) / 150 * 100), 2)}%"
                            if not column_for_fill:
                                column_for_fill = column
                            processed_records.append(record)
                            break
                        else:                                          #If Total > 150 fill "-"
                            work_frame.at[index, column] = "-"
                            if not column_for_fill:
                                column_for_fill = column
                            processed_records.append(record)
                            break
                break
    without_match = [record for record in datas if record not in processed_records] # New records
    if last_row_index: #Fill new records
        new_index = work_frame.loc[last_row_index]["Column1"]
        for new_record in without_match:
            row_index = new_index
            new_row = {"Column1": str(int(row_index)+1),
                       "Column2": new_record['name'],
                           }
            new_index= str(int(new_index)+1)
            if int(column_for_fill[1:])>=10:
                for i in range(1,10):
                    new_row.update({f"R0{i}": "-"})
                for i in range(10,int(column_for_fill[1:])):
                    new_row.update({f"R{i}": "-"})
                for i in range((int(column_for_fill[1:])+2),(last_r_column+2)):
                    new_row.update({f"R{i}": pd.NA})
            else:
                for i in range(int(column_for_fill[1:])):
                    new_row.update({f"R0{i}": "-"})
                for i in range((int(column_for_fill[1:])+2),(last_r_column+2)):
                    new_row.update({f"R{i}": pd.NA})
            if new_record['score']<=150.0:
                new_row.update({column_for_fill: new_record['score']})
                new_row.update({"Total": new_record['score']})
                new_row.update({"Spent": (150.0 - new_record['score'])})
                new_row.update({"Percent": f"{round(((150.0 - new_record['score']) / 150 * 100), 2)}%"})
            else:
                new_row.update({column_for_fill: "-"})
                new_row.update({"Total": pd.NA})
                new_row.update({"Spent": pd.NA})
                new_row.update({"Percent": pd.NA})

            work_frame = pd.concat([
                work_frame.iloc[:-2],
                pd.DataFrame([new_row]),
                work_frame.iloc[-2:]
            ])

                                                                     # Check second table records for our sort
    list_for_sort = []
    none_list = []
    for index, row in work_frame.iterrows():
        if pd.isna(row.to_dict()['Column1']):
            none_list.append(row.to_dict())
        else:
            list_for_sort.append(row.to_dict())

    sorted_result = sorter(list_for_sort)            #Sorting
    sorted_result = pd.DataFrame(sorted_result)
    none_list = pd.DataFrame(none_list)
    final_work_frame = pd.concat([sorted_result, none_list]) #append all frames in second table


    leaderboard_frame = leaderboard_frame.iloc[:(int(empty_fields[-1]) + 2)]
    leaderboard_frame = pd.concat([leaderboard_frame, final_work_frame]) # Append all frames in new table

    leaderboard_frame.to_csv(leaderboard_csv, index=False) # Save our frame

if __name__ == '__main__':
    csv_parser("leaderboard_file_path","new_data_file_path")
