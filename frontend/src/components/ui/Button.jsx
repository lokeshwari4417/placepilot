import PropTypes from "prop-types";

const VARIANTS = {
  primary: "bg-accent-600 text-white hover:bg-accent-700",
  secondary: "bg-slate-100 text-ink hover:bg-slate-200",
  ghost: "text-muted hover:text-ink hover:bg-slate-100",
};

export function Button({ variant = "primary", className = "", children, ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${VARIANTS[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

Button.propTypes = {
  variant: PropTypes.oneOf(["primary", "secondary", "ghost"]),
  className: PropTypes.string,
  children: PropTypes.node.isRequired,
};
