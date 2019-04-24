using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
        PythonInterface pythonInterface;
        private void Form1_Load(object sender, EventArgs e)
        {
            client = new SimpleTCP.SimpleTcpClient();
            client.StringEncoder = Encoding.UTF8;

            pythonInterface = new PythonInterface();
        }

        private void Button1_Click_1(object sender, EventArgs e)
        {
            client.Connect(textHost.Text, int.Parse(textPort.Text));
            var replyMsg = client.WriteLineAndGetReply(pythonInterface.makeDecision(), TimeSpan.FromSeconds(10));
            textStatus.Invoke((MethodInvoker)delegate ()
            {
                textStatus.Text += replyMsg.MessageString;
            });
        }
    }
}
