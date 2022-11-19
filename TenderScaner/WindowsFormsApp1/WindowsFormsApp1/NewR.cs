using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    static class NewR
    {
        public static int AddRow(this TableLayoutPanel table, RowStyle rowStyle = null, params string[] rowData)
        {
            List<Label> labels = new List<Label>();
            rowData.ToList().ForEach(p => labels.Add(new Label() { Text = p }));
            return table.AddRow(rowStyle, labels.ToArray());
        }

        public static int AddRow(this TableLayoutPanel table, RowStyle rowStyle = null, params Control[] rowData )
        {
            table.RowCount += 1;

            if (rowStyle == null)
            {
                rowStyle = new RowStyle(SizeType.Absolute , 250);
                //rowStyle.Height = 250;
            }
            rowStyle = new RowStyle(SizeType.Absolute , 100);


            table.RowStyles.Add(rowStyle);
            
            for (int i = 0; i < rowData.Length; i++)
            {
                if (i > table.ColumnCount - 1)
                    break;

                if (rowData.Length == 1)
                {
                    table.Controls.Add(rowData[i], 1, table.RowCount);

                } else if (rowData.Length != 1) {

                    table.Controls.Add(rowData[i], i, table.RowCount);
                }
            }

            return table.RowCount ;
        }

        public static int AddColumn(this TableLayoutPanel table, ColumnStyle columnStyle = null, params string[] columnData)
        {
            List<Label> labels = new List<Label>();
            columnData.ToList().ForEach(p => labels.Add(new Label() { Text = p }));
            return table.AddColumn(columnStyle, labels.ToArray());
        }

        public static int AddColumn(this TableLayoutPanel table, ColumnStyle columnStyle = null, params Control[] columnData)
        {
            table.ColumnCount += 1;

            if (columnStyle == null)
                columnStyle = new ColumnStyle(SizeType.AutoSize);

            table.ColumnStyles.Add(columnStyle);

            for (int i = 0; i < columnData.Length; i++)
            {
                if (i > table.RowCount - 1)
                    break;

                table.Controls.Add(columnData[i], table.ColumnCount - 1, i);
            }

            return table.ColumnCount - 1;
        }
    }
}
