from pandas import DataFrame, ExcelWriter


def write_styling_excel(path: str, df: DataFrame, sheet_name: str, index=False):
    """pip install xlsxwriter
    форматируем колонки файла эксель"""

    with ExcelWriter(path, engine="xlsxwriter") as wb:
        df.to_excel(wb, sheet_name=sheet_name, index=index, header=False, startrow=1)
        sheet = wb.sheets[sheet_name]

        cell_format = wb.book.add_format()
        cell_format.set_font_color("white")
        cell_format.set_bg_color("#AAAAAA")
        cell_format.set_font_size(14)
        cell_format.set_bold()

        for col, name in enumerate(df.columns):
            try:
                width = max(df[name].astype(str).map(len).max(), len(name))
            except:
                width = 40

            width = {
                width > 45: 45,
                width < 20: 20,
            }.get(True, width)

            sheet.write(0, col, name, cell_format)
            sheet.set_column(0, col, width)
        sheet.autofilter(0, 0, df.shape[0], len(df.columns) - 1)
