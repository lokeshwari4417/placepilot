import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../api/client";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "", role: "student" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await apiClient.post("/auth/register/", form);
      navigate("/login");
    } catch (err) {
      setError("Could not create account. Please check your details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Email" type="email" name="email" value={form.email} onChange={handleChange} required />
      <Input label="Password" type="password" name="password" value={form.password} onChange={handleChange} required />
      {error && <p className="text-sm text-red-600">{error}</p>}
      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? "Creating account..." : "Create account"}
      </Button>
      <p className="text-sm text-muted text-center">
        Already have an account? <Link to="/login" className="text-accent-600 hover:underline">Sign in</Link>
      </p>
    </form>
  );
}
