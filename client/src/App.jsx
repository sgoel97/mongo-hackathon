import { useState, useEffect, useRef } from "react";
import recruiterURL from "./assets/recruiter.jpg";
import ChatBox from "./ChatBox";
import ResumeBox from "./ResumeBox";
import { motion } from "framer-motion";
import axios from "axios";

const App = () => {
  const resumeUploadRef = useRef();

  const uploadResume = async () => {
    const formData = new FormData();
    formData.append("file", resumeUploadRef.current.files[0]);

    await axios.post("/api/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    await updateFiles();
  };

  const updateFiles = async () => {
    const { data } = await axios.get("/api/upload");
    setFilenames(data.files);
  };

  const [filenames, setFilenames] = useState(null);
  useEffect(() => {
    updateFiles().catch(console.error);
  }, []);

  return (
    <>
      <header className="px-12 py-6 flex justify-end">
        <div className="flex items-center gap-4">
          <img
            src={recruiterURL}
            className="w-9 h-9 object-cover rounded-full"
          />
          <div className="leading-tight text-sm">
            <div className="font-medium">Timothy Guo</div>
            <div className="text-slate-700">Tech Recruiter</div>
          </div>
        </div>
      </header>
      <main className="mx-auto my-0 max-w-xl py-8">
        <div>
          <h1 className="text-5xl mb-1">Welcome to ResumeAG</h1>
          <h2 className="text-5xl font-light text-gray-500">
            Find your perfect candidate!
          </h2>
        </div>
        <div className="mt-8">
          <input
            ref={resumeUploadRef}
            multiple={false}
            type="file"
            hidden
            onChange={uploadResume}
          />
          <button
            className="py-2 px-4 text-sm font-medium text-white bg-slate-800 shadow-xl active:scale-95 transition"
            onClick={() => resumeUploadRef.current?.click()}
          >
            Upload Resume&nbsp;&nbsp;→
          </button>
        </div>
        <div className="mt-8">
          <h3 className="font-medium text-slate-500">All Resumes</h3>
          <motion.div
            className="flex flex-wrap gap-4 mt-2"
            variants={{
              show: {
                transition: {
                  staggerChildren: 0.05,
                },
              },
            }}
            animate="show"
          >
            {filenames ? (
              filenames.map((filename, i) => (
                <ResumeBox filename={filename} key={i} />
              ))
            ) : (
              <div className="loading" />
            )}
          </motion.div>
        </div>
        <div className="fixed bottom-16 left-0 right-0">
          <div className="mx-auto my-0 max-w-xl">
            <ChatBox onSubmit={() => void 0} />
          </div>
        </div>
      </main>
    </>
  );
};

export default App;
