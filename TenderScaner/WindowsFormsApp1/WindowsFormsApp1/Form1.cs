using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using static WindowsFormsApp1.NewR;

using Sl.Selenium.Extensions.Chrome;
using System.Net;
using System.Threading;

namespace WindowsFormsApp1
{
    
    public partial class Form1 : Form
    {
        //Sample 02: Process for the batch
        private Process BatchProc = null;
        public Form1() => InitializeComponent();

        private void tableLayoutPanel4_Paint(object sender, PaintEventArgs e)
        {

        }

        public Bitmap GetImageFromUrl(string imageUrl)
        {
            if (imageUrl.Length == 0)
                return null;
            using (WebClient client = new WebClient())
            {
                using (Stream stream = client.OpenRead(imageUrl))
                    return new Bitmap(stream);
            }                  
        }


        private void button1_Click(object sender, EventArgs e)
        {
            string[] str = new string[2];
            str[0] = "sd";
            str[1] = "sd";
            if (clearTableCheckBox.Checked == true) ClearTable();
            StartChecking();
            if (Ural_In_checkbox.Checked == true)
                GetResultFromBuffer(@"../../../../../buffer/Ural_In.txt");

            if (Orbita_Zip_checkbox.Checked == true)
                GetResultFromBuffer(@"../../../../../buffer/Orbita_Zip.txt");

            if (Forumauto_checkbox.Checked == true)
                GetResultFromBuffer(@"../../../../../buffer/Forumauto.txt");

            if (Autoklad_checkbox.Checked == true)
                GetResultFromBuffer(@"../../../../../buffer/Autoklad.txt");

            //Thread.Sleep(30000);
            
            //tableLayoutPanel1.ColumnStyles.Add( new ColumnStyle(SizeType.Absolute, 40));
            //tableLayoutPanel1.Controls.Add(new Label() { Text = "Street, City, State" }, 1, 1);

            //string stringString = "Mahesh Chand, Neel Chand Beniwal, Raj Beniwal, Dinesh Beniwal";
            // String separator  

            //NewR.AddRow(tableLayoutPanel1, new RowStyle(SizeType.Absolute, 50F), con);
        }

        private void GetResultFromBuffer(string path)
        {
            Control[] con = new Control[4];
            Control[] EmptyCon = new Control[1];
            EmptyCon[0] = new Label() { Text = "________" };
            Encoding encoding = Encoding.GetEncoding("windows-1251");
            using (StreamReader sr = new StreamReader(path, encoding))
            {
                string s;
                string stringString = "";
                string[] stringSeparators = null;
                string[] firstNames = null;
                while ((s = sr.ReadLine()) != null)
                {
                    stringString = s;
                    stringSeparators = new string[] { " $%$," };
                    firstNames = stringString.Split(stringSeparators, StringSplitOptions.None);
                    con[0] = new PictureBox()
                    {
                        Image = GetImageFromUrl(firstNames[4].Substring(10)),
                        SizeMode = PictureBoxSizeMode.Zoom,
                        Dock = DockStyle.Fill
                    };
                    con[1] = new RichTextBox() { Text = firstNames[1], ReadOnly = true, Dock = DockStyle.Fill };
                    con[2] = new TextBox() { Text = firstNames[2], ReadOnly = true, Dock = DockStyle.Fill };
                    con[3] = new Label() { Text = firstNames[3] };
                    NewR.AddRow(tableLayoutPanel1, new RowStyle(SizeType.Absolute, 50F), con);
                }
                NewR.AddRow(tableLayoutPanel1, new RowStyle(SizeType.Absolute, 10F), EmptyCon);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            StartChecking();

        }

        private void StartChecking()
        {
            if (Ural_In_checkbox.Checked == true)
                StartBatFile(@"..\..\..\..\..\Ural_In\");

            if (Orbita_Zip_checkbox.Checked == true)
                StartBatFile(@"..\..\..\..\..\Orbita_Zip\");

            if (Forumauto_checkbox.Checked == true)
                StartBatFile(@"..\..\..\..\..\Forumauto\");

            if (Autoklad_checkbox.Checked == true)
                StartBatFile(@"..\..\..\..\..\Autoklad\");
        }

        private static void StartBatFile(string path)
        {
            using (Process proc = new Process())
            {
                proc.StartInfo.WorkingDirectory = path;
                proc.StartInfo.FileName = "command.bat";
                proc.StartInfo.CreateNoWindow = true;
                proc.Start();
                proc.WaitForExit();
                proc.Close();
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            ClearTable();
        }

        private void ClearTable()
        {
            tableLayoutPanel1.Controls.Clear();
            tableLayoutPanel1.RowStyles.Clear();
            tableLayoutPanel1.RowCount = 1;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 20F));
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            string path = @"../../../../../buffer/naming.txt";

            Encoding encoding = Encoding.GetEncoding("windows-1251");
            using (StreamWriter sw = new StreamWriter(path,false , encoding))
            {
                sw.Write(textBox1.Text);
                    
            }
            
            /*
            // Open the file to read from.
            using (StreamReader sr = File.OpenText(path))
            {
                string s;
                while ((s = sr.ReadLine()) != null)
                {
                    Console.WriteLine(s);
                }
            }
            */
        }
    }
}
