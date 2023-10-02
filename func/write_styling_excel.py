from pandas import DataFrame, ExcelWriter


def write_styling_excel(path: str, df: DataFrame, sheet_name: str, index=False):
    """pip install xlsxwriter
    форматируем колонки файла эксель"""

    with ExcelWriter(path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index, na_rep="NaN")
        # автонастройка ширины колонок
        for column in df:
            try:
                width = max(df[column].astype(str).map(len).max(), len(column))
            except:
                width = 45

            width = {
                width > 45: 45,
                width < 20: 20,
            }.get(True, width)

            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, width)
