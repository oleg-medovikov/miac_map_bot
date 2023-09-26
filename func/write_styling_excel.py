from pandas import DataFrame, ExcelWriter


def write_styling_excel(path: str, df: DataFrame, sheet_name: str, index=False):
    "форматируем колонки файла эксель"
    with ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index, na_rep="NaN")

        # автонастройка ширины колонок
        # решил что больше ничего и не нужно
        for column in df:
            try:
                width = max(df[column].astype(str).map(len).max(), len(column))
            except:
                width = 45

            if width > 45:
                width = 45
            if width < 20:
                width = 20

            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, width)

        writer.save()
