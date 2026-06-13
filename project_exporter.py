# ==========================================
# Excel Export Module
# ==========================================

import pandas as pd


class ExcelExporter:

    def save_products(
        self,
        products,
        filename
    ):

        if not products:
            raise Exception(
                "No products found"
            )

        products = [
            p for p in products
            if p
        ]

        df = pd.DataFrame(products)

        df.drop_duplicates(
            inplace=True
        )

        with pd.ExcelWriter(
            filename,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Products"
            )

            worksheet = writer.sheets[
                "Products"
            ]

            for column in worksheet.columns:

                max_length = 0

                column_letter = (
                    column[0].column_letter
                )

                for cell in column:

                    try:

                        if len(
                            str(cell.value)
                        ) > max_length:

                            max_length = len(
                                str(cell.value)
                            )

                    except:
                        pass

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 5,
                    80
                )
                
        return filename

