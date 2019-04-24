using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TCIP_forms_interface
{
    public class PythonInterface
    {
        public String makeDecision()
        {
            return "";
        }

        private int askTheAI(int[,] grid)
        {
            return 0;
        }

        private int[,] seeGrid()
        {
            String stream = run_python_code("python", "wagner.py");
            var grid = new int[6, 7];
            //TODO: parse strem into grid
            return grid;
        }

        private String run_python_code(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "PATH_TO_PYTHON_EXE";
            start.Arguments = string.Format("\"{0}\" \"{1}\"", cmd, args);
            start.UseShellExecute = false;
            start.CreateNoWindow = true; 
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string stderr = process.StandardError.ReadToEnd();
                    string result = reader.ReadToEnd();
                    return result;
                }
            }
        }
    }
}
