import { motion } from "framer-motion";

const ResumeBox = ({ filename }) => (
  <motion.div
    initial={{ opacity: 0.1, y: 20 }}
    variants={{ show: { opacity: 1, y: 0 } }}
    className="shadow-lg bg-slate-200 px-3 py-2"
  >
    <span className="font-mono font-light text-slate-700 text-sm">
      {filename}
    </span>
  </motion.div>
);

export default ResumeBox;
