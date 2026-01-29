import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { from: "user", text: input }]);
    setLoading(true);
    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input })
      });
      const data = await res.json();
      setMessages((msgs) => [...msgs, { from: "bot", text: data.text || data.detail || JSON.stringify(data) }]);
    } catch (err) {
      setMessages((msgs) => [...msgs, { from: "bot", text: "Erreur de connexion à l'API." }]);
    }
    setInput("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Chat avec Gemini</h2>
      <div style={{ border: "1px solid #ccc", padding: 16, minHeight: 200, marginBottom: 16 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.from === "user" ? "right" : "left" }}>
            <b>{msg.from === "user" ? "Vous" : "Bot"}:</b> {msg.text}
          </div>
        ))}
        {loading && <div>Envoi...</div>}
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          style={{ flex: 1, marginRight: 8 }}
          placeholder="Posez une question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>Envoyer</button>
      </form>
    </div>
  );
}

export default App;
