using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using SimpleTCP;

namespace TCIP_forms_interface
{
    public partial class ClientForm : Form
    {
        public ClientForm()
        {
            InitializeComponent();
        }

        SimpleTCP.SimpleTcpClient client;
        private void Form1_Load(object sender, EventArgs e)
        {
            client = new SimpleTCP.SimpleTcpClient();
            client.StringEncoder = Encoding.UTF8;

        }

        private void Button1_Click_1(object sender, EventArgs e)
        {
            textStatus.Invoke((MethodInvoker)delegate ()
            {
                string decision = System.IO.File.ReadAllText(@"C:\Users\pdevasconcellos\source\repos\IndustrialRobotics\TCIP_forms_interface\TCIP_forms_interface\pysource\decision.txt");
                textStatus.Text += "Started client. Testing AI interface" + decision;
            });
            /*
            client.Connect(textHost.Text, int.Parse(textPort.Text));
            var replyMsg = client.WriteLineAndGetReply(pythonInterface.makeDecision(), TimeSpan.FromSeconds(10));
            textStatus.Invoke((MethodInvoker)delegate ()
            {
                textStatus.Text += replyMsg.MessageString;
            });*/
        }
    }
}
