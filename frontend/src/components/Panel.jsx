import { motion } from "framer-motion";

export default function Panel({ title, subtitle, children, className = "" }) {
  return (
    <motion.section
      className={`panel ${className}`}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      {(title || subtitle) && (
        <div className="panel-head">
          <div>
            {title && <h2>{title}</h2>}
            {subtitle && <p>{subtitle}</p>}
          </div>
        </div>
      )}

      {children}
    </motion.section>
  );
}