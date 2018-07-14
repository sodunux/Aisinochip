using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace DataCal
{
    public partial class DataCal : Form
    {
        byte[] databuff = new byte[1024 * 1024];
        int databufflen = 0;

        public DataCal()
        {
            InitializeComponent();
        }

        private void DataCal_Load(object sender, EventArgs e)
        {

        }

        public static string DeleteSpaceString(string hexString)
        {
            hexString = hexString.Replace(" ", "");
            hexString = hexString.Replace("\t", "");
            if ((hexString.Length % 2) != 0)
                hexString = "0" + hexString; //如果最后不足两位，最后添“0”。

            return hexString;
        }
        public static byte[] strToHexByte(string hexString)
        {
            hexString = hexString.Replace(" ", "");
            if ((hexString.Length % 2) != 0)
                hexString = "0" + hexString;  //如果最后不足两位，最后添“0”。
            byte[] returnBytes = new byte[hexString.Length / 2];
            for (int i = 0; i < returnBytes.Length; i++)
                returnBytes[i] = Convert.ToByte(hexString.Substring(i * 2, 2), 16);
            return returnBytes;
        }
        public static string byteToHexStr(int len, byte[] bytes)
        {
            string returnStr = "";
            if (bytes != null)
            {
                for (int i = 0; i < len; i++)
                {
                    returnStr += bytes[i].ToString("X2");
                }
            }
            return returnStr;
        }

        public void showMessage(string tempstr) 
        {
            richTextBox1.Text += tempstr;
            richTextBox1.Text += "\n";
        }

        public int calcrc(byte[] data,int initvalue,int len)
        {
            int i,j;
            int result;
            result = initvalue;
            for (i = 0; i < len; i++)
            {
                result = result ^ data[i];
                for (j = 0; j < 8; j++)
                {
                    if ((result & 0x0001) == 0x0001)
                        result = (result >> 1) ^ 0x8408;
                    else
                        result = result >> 1;
                }
            }
            return result;
        }

        void updatedatabuff()
        {
            int i,j;
            string tempstr;
            databufflen = 0;
            byte[] tempbuff=new byte[16];
            try
            {
                for (i = 0; i < dataGridView1.RowCount; i++)
                {
                    
                    tempstr = dataGridView1[1, i].Value.ToString();
                    tempstr = DeleteSpaceString(tempstr);
                    tempbuff = strToHexByte(tempstr);
                    for (j = 0; j < 16; j++) 
                    {
                        databuff[databufflen + j] = tempbuff[j];
                    }
                    databufflen += 16;    
                }
            }
            finally 
            {
                //showMessage("读取缓存区数据错误");
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string filename;
            string tempstr;
            string[] rowcode;
            int i,j;
            string addrstr;
            string datacountstr;
            string szHex;
            int hexbaseaddr;
            byte[] bytedata;
            int addr;


            openFileDialog1.Filter = "hex files (*.hex;*.bin)|*.bin;*.hex|All files (*.*)|*.*";
            openFileDialog1.ShowDialog();
            filename = openFileDialog1.FileName;
            tempstr = filename.Substring(filename.Length - 4, 4);
            tempstr = tempstr.ToUpper();
            hexbaseaddr = 0;
            try 
            {
                if (tempstr == ".HEX")
                {
                    rowcode = File.ReadAllLines(filename);

                    for (i = 0; i < rowcode.Length; i++)
                    {
                        szHex = "";
                        tempstr = rowcode[i];
                        if (tempstr == "")
                            continue;
                        else if (tempstr.Substring(0, 1) == ":")
                        {
                            if (tempstr.Substring(1, 8) == "00000001")
                                break;
                            else if (tempstr.Substring(7, 2) == "02") //段偏移 地址偏移4bits
                            {
                                hexbaseaddr = Convert.ToUInt16(tempstr.Substring(9, 4), 16) << 0x04;
                                continue;
                            }
                            else if (tempstr.Substring(7, 2) == "04") //线性段偏移 地址偏移16bits
                            {
                                hexbaseaddr = Convert.ToUInt16(tempstr.Substring(9, 4), 16) << 16;
                            }
                            else if (tempstr.Substring(7, 2) == "05")
                            {
                            }
                            else if (tempstr.Substring(7, 2) == "03") { }
                            else
                            {
                                addrstr = tempstr.Substring(3, 4);//记录该行地址
                                datacountstr = tempstr.Substring(1, 2);//记录该行的字节个数
                                szHex += tempstr.Substring(9, tempstr.Length - 11);//读取数据
                                bytedata = strToHexByte(szHex);
                                //addr = hexbaseaddr + (int)(strToHexByte(addrstr)[1]) + (int)(strToHexByte(addrstr)[0] * 256);
                                addr = (int)(strToHexByte(addrstr)[1]) + (int)(strToHexByte(addrstr)[0] * 256);
                                if (addr >= databufflen)
                                {
                                    databufflen = addr + strToHexByte(datacountstr)[0];
                                }
                                for (j = 0; j < strToHexByte(datacountstr)[0]; j++)
                                {
                                    databuff[addr + j] = bytedata[j];
                                }
                            }
                        }
                    }
                    databufflen = ((databufflen + 3) / 4) * 4; //文件大小取4的倍数
                }
                else if (tempstr == ".BIN")
                {
                    FileStream s2 = File.OpenRead(filename);
                    databufflen = (int)s2.Length;
                    s2.Read(databuff, 0, databufflen);
                    s2.Close();
                    databufflen = ((databufflen + 3) / 4) * 4;
                }
                else { }

                //显示数据
                dataGridView1.Rows.Clear();//清除数据buffer
                if (databufflen == 0) dataGridView1.RowCount = 1;
                else dataGridView1.RowCount = ((databufflen + 15) / 16);

                for (i = 0; i < dataGridView1.RowCount; i++)
                {
                    dataGridView1[0, i].Value = (i * 16 + hexbaseaddr).ToString("X8");
                    tempstr = "";
                    for (j = 0; j < 0x10; j++)
                    {
                        tempstr = tempstr + databuff[i * 16 + j].ToString("X2") + " ";
                    }
                    dataGridView1[1, i].Value = tempstr;
                }
            }
            finally
            {
                //showMessage("打开文件失败");
            }
            
         }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void CrcBtn_Click(object sender, EventArgs e)
        {
            byte []endaddrbytes=new byte[4];
            byte []initvaluebytes=new byte[4];
            int len,initvalue;
            int crcvalue;
            string tempstr;
            try 
            {
                updatedatabuff();
                
                endaddrbytes=strToHexByte(textBox2.Text);
                initvaluebytes=strToHexByte(textBox1.Text);
                initvalue=(int)initvaluebytes[1] + (int)initvaluebytes[0] * 256;
                len=(int)(endaddrbytes[3]) + (int)(endaddrbytes[2] <<8)+(int)(endaddrbytes[1] <<16)+(int)(endaddrbytes[2] <<24)+1;
                crcvalue=calcrc(databuff, initvalue, len);
                tempstr = "CRC初始值：" + initvalue.ToString("X8")+"\n";
                tempstr += "CRC计算长度：" + len.ToString("X8") + "\n";
                tempstr += "CRC计算结果：" + crcvalue.ToString("X8");
                showMessage(tempstr);       
            }
            finally {
                //showMessage("CRC计算错误");
            }
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }
        
        


    }

}
