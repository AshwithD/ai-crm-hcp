import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { mergeInteraction } from "./interactionSlice";

function App() {
  const interaction = useSelector((state) => state.interaction);
  const dispatch = useDispatch();
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("https://ai-crm-hcp.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await res.json();
      dispatch(mergeInteraction(data));
    } catch (e) {
      alert("Backend not reachable. Is FastAPI running?");
      console.error(e);
    } finally {
      setMessage("");
      setLoading(false);
    }
  };

  const Card = ({ title, children }) => (
    <div
      style={{
        background: "#ffffff",
        borderRadius: 14,
        padding: 16,
        marginBottom: 16,
        boxShadow: "0 6px 16px rgba(0,0,0,0.08)"
      }}
    >
      <h3 style={{ marginBottom: 12, color: "#0f172a" }}>{title}</h3>
      {children}
    </div>
  );

  const Field = ({ label, value, placeholder }) => (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: 12, color: "#475569", marginBottom: 4 }}>{label}</div>
      <div
        style={{
          padding: "10px 12px",
          border: "1px solid #e5e7eb",
          borderRadius: 10,
          background: "#f8fafc",
          minHeight: 42,
          color: "#0f172a"
        }}
      >
        {Array.isArray(value)
          ? value.length
            ? value.join(", ")
            : placeholder
          : value || placeholder}
      </div>
    </div>
  );

  const SentimentChips = ({ value }) => {
    const map = {
      positive: { label: "🙂 Positive", color: "#dcfce7", border: "#22c55e" },
      neutral: { label: "😐 Neutral", color: "#e0f2fe", border: "#0284c7" },
      negative: { label: "🙁 Negative", color: "#fee2e2", border: "#ef4444" }
    };

    return (
      <div style={{ display: "flex", gap: 10 }}>
        {["positive", "neutral", "negative"].map((k) => (
          <div
            key={k}
            style={{
              padding: "8px 12px",
              borderRadius: 999,
              border: value === k ? `2px solid ${map[k].border}` : "1px solid #e5e7eb",
              background: value === k ? map[k].color : "#ffffff",
              fontWeight: value === k ? 600 : 400,
              color: "#0f172a"
            }}
          >
            {map[k].label}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        padding: 16,
        background: "linear-gradient(180deg, #eef2ff 0%, #f8fafc 100%)",
        fontFamily: "Inter, system-ui, sans-serif"
      }}
    >
      <h1 style={{ marginBottom: 12, color: "#0f172a" }}>Log HCP Interaction</h1>

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 16, height: "calc(100% - 56px)" }}>
        {/* LEFT PANEL */}
        <div style={{ overflowY: "auto", paddingRight: 6 }}>
          <Card title="Interaction Details">
            <Field label="HCP Name" value={interaction.hcp_name} placeholder="Auto-filled by AI" />
            <Field label="Topics Discussed" value={interaction.topics_discussed} placeholder="Auto-filled by AI" />
            <Field label="Materials Shared" value={interaction.materials_shared} placeholder="Auto-filled by AI" />
            <Field label="Samples Distributed" value={interaction.samples_distributed} placeholder="Auto-filled by AI" />

            <div style={{ marginTop: 8 }}>
              <div style={{ fontSize: 12, color: "#475569", marginBottom: 6 }}>
                Observed / Inferred HCP Sentiment
              </div>
              <SentimentChips value={interaction.sentiment} />
            </div>

            <Field label="Outcomes" value={interaction.outcomes} placeholder="Auto-filled by AI" />
            <Field label="Follow-ups" value={interaction.followups} placeholder="Auto-filled by AI" />
          </Card>

          <Card title="HCP History">
            <Field label="Last Interaction Date" value={interaction.last_interaction} placeholder="No history yet" />
            <Field label="Last Topic" value={interaction.last_topic} placeholder="No history yet" />
            <Field label="Last Sentiment" value={interaction.last_sentiment} placeholder="No history yet" />
          </Card>

          <Card title="Compliance">
            <Field
              label="Compliance Issues"
              value={interaction.compliance_issues}
              placeholder="No issues detected"
            />
          </Card>
        </div>

        {/* RIGHT PANEL */}
        <div
          style={{
            background: "#0f172a",
            borderRadius: 16,
            padding: 16,
            display: "flex",
            flexDirection: "column",
            boxShadow: "0 10px 20px rgba(0,0,0,0.15)"
          }}
        >
          <h3 style={{ color: "#e5e7eb" }}>AI Assistant</h3>
          <p style={{ color: "#94a3b8", fontSize: 13, marginBottom: 8 }}>
            Log interaction via chat
          </p>

          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder='Describe interaction... (e.g. "Met Dr. Smith, positive sentiment, shared brochure")'
            style={{
              flex: 1,
              resize: "none",
              padding: 12,
              borderRadius: 10,
              border: "1px solid #334155",
              marginBottom: 10,
              background: "#020617",
              color: "#e5e7eb",
              caretColor: "#e5e7eb"
            }}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            style={{
              padding: "10px 16px",
              borderRadius: 10,
              border: "none",
              background: loading ? "#64748b" : "#2563eb",
              color: "#ffffff",
              fontWeight: 600,
              cursor: loading ? "not-allowed" : "pointer"
            }}
          >
            {loading ? "Thinking..." : "Log"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
