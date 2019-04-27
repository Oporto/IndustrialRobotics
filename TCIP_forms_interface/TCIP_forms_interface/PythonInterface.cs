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
            return askTheAI(seeGrid());
        }

        private String askTheAI(String grid)
        {
            var cmd = "python";
            var args = "alpha_beta_agent.py " + grid;

            return run_python_code(cmd, args);
        }

        private String seeGrid()
        {
            String grid = run_python_code("python", "CameraVision.py");
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
