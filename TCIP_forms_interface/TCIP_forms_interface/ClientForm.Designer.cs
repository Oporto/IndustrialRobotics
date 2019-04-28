using System;

namespace TCIP_forms_interface
{
    partial class ClientForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.HostLab = new System.Windows.Forms.Label();
            this.textHost = new System.Windows.Forms.TextBox();
            this.textPort = new System.Windows.Forms.TextBox();
            this.labelPort = new System.Windows.Forms.Label();
            this.textStatus = new System.Windows.Forms.TextBox();
            this.labelStatus = new System.Windows.Forms.Label();
            this.nextTurnBnt = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // HostLab
            // 
            this.HostLab.AutoSize = true;
            this.HostLab.Location = new System.Drawing.Point(40, 63);
            this.HostLab.Name = "HostLab";
            this.HostLab.Size = new System.Drawing.Size(47, 20);
            this.HostLab.TabIndex = 1;
            this.HostLab.Text = "Host:";
            this.HostLab.Click += new System.EventHandler(this.Label1_Click);
            // 
            // textHost
            // 
            this.textHost.Location = new System.Drawing.Point(93, 60);
            this.textHost.Name = "textHost";
            this.textHost.Size = new System.Drawing.Size(118, 26);
            this.textHost.TabIndex = 2;
            this.textHost.Text = "192.168.100.100";
            this.textHost.TextChanged += new System.EventHandler(this.TextBox1_TextChanged);
            // 
            // textPort
            // 
            this.textPort.Location = new System.Drawing.Point(276, 60);
            this.textPort.Name = "textPort";
            this.textPort.Size = new System.Drawing.Size(69, 26);
            this.textPort.TabIndex = 5;
            this.textPort.Text = "5000";
            this.textPort.TextChanged += new System.EventHandler(this.TextBox2_TextChanged);
            // 
            // labelPort
            // 
            this.labelPort.AutoSize = true;
            this.labelPort.Location = new System.Drawing.Point(228, 63);
            this.labelPort.Name = "labelPort";
            this.labelPort.Size = new System.Drawing.Size(42, 20);
            this.labelPort.TabIndex = 4;
            this.labelPort.Text = "Port:";
            this.labelPort.Click += new System.EventHandler(this.Label2_Click);
            // 
            // textStatus
            // 
            this.textStatus.Location = new System.Drawing.Point(44, 140);
            this.textStatus.Multiline = true;
            this.textStatus.Name = "textStatus";
            this.textStatus.Size = new System.Drawing.Size(443, 133);
            this.textStatus.TabIndex = 8;
            this.textStatus.TextChanged += new System.EventHandler(this.TextStatus_TextChanged);
            // 
            // labelStatus
            // 
            this.labelStatus.AutoSize = true;
            this.labelStatus.Location = new System.Drawing.Point(40, 105);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(60, 20);
            this.labelStatus.TabIndex = 9;
            this.labelStatus.Text = "Status:";
            // 
            // nextTurnBnt
            // 
            this.nextTurnBnt.Location = new System.Drawing.Point(374, 63);
            this.nextTurnBnt.Name = "nextTurnBnt";
            this.nextTurnBnt.Size = new System.Drawing.Size(113, 62);
            this.nextTurnBnt.TabIndex = 10;
            this.nextTurnBnt.Text = "Next Turn";
            this.nextTurnBnt.UseVisualStyleBackColor = true;
            this.nextTurnBnt.Click += new System.EventHandler(this.Button1_Click_1);
            // 
            // ClientForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(535, 324);
            this.Controls.Add(this.nextTurnBnt);
            this.Controls.Add(this.labelStatus);
            this.Controls.Add(this.textStatus);
            this.Controls.Add(this.textPort);
            this.Controls.Add(this.labelPort);
            this.Controls.Add(this.textHost);
            this.Controls.Add(this.HostLab);
            this.Name = "ClientForm";
            this.Text = "Client";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        private void TextStatus_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void Label2_Click(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }

        private void TextBox2_TextChanged(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }

        private void TextBox1_TextChanged(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }

        private void Label1_Click(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }

        #endregion
        private System.Windows.Forms.Label HostLab;
        private System.Windows.Forms.TextBox textHost;
        private System.Windows.Forms.TextBox textPort;
        private System.Windows.Forms.Label labelPort;
        private System.Windows.Forms.TextBox textStatus;
        private System.Windows.Forms.Label labelStatus;
        private System.Windows.Forms.Button nextTurnBnt;
    }
}

