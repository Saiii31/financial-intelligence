import { useState } from 'react';
import { Bot, Send } from 'lucide-react';
import { askFinancialQuestion, USE_MOCK_DATA } from '../services/api';

const SUGGESTIONS = [
  'How much did I spend on food last month?',
  'What\'s my debt situation?',
  'Why did my savings drop?',
  'What should I do to improve my finances?',
  'Show me my highest expense category',
  'What\'s my financial health score?',
];

export default function AIChat() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function submitQuestion(text) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    setError(null);
    setLoading(true);
    setHistory((h) => [...h, { role: 'user', text: trimmed }]);
    setQuestion('');

    try {
      if (USE_MOCK_DATA) {
        await new Promise((r) => setTimeout(r, 600));
        // Provide helpful mock responses based on the question
        const mockResponses = {
          'how much did i spend on food last month?': 'Based on your transaction data, you spent ₹61,003.50 on food last month, which is 11.9% of your total expenses.',
          'what\'s my debt situation?': 'You have 3 liabilities totaling ₹3,338,000: Home Loan (₹2,850,000 @ 8.35%), Car Loan (₹420,000 @ 9.1%), and Credit Card (₹68,000 @ 32%). Your total monthly EMI is ₹46,700.',
          'why did my savings drop?': 'Your savings dropped this month due to increased expenses (₹3,761,663 in March 2026 vs ₹1,757,857 in February). This was mainly due to a large utility payment of ₹189,900.',
          'what should i do to improve my finances?': 'Focus on: 1) Paying down your high-interest credit card (32%) first, 2) Maintain your current savings rate of 17.56%, 3) Review spending in Debt Payment category (20.8% of expenses).',
          'show me my highest expense category': 'Your highest expense category is Debt Payment at ₹1,053,005.71 (20.8% of total expenses), followed by Housing at ₹768,000 (15.0%).',
          'what\'s my financial health score?': 'Your overall financial health score is 83.2/100. This is considered good! Your debt score is excellent (100), savings score is 60, and cash flow score is 100.',
        };
        
        const lowerQuestion = trimmed.toLowerCase();
        const response = Object.keys(mockResponses).find(key => lowerQuestion.includes(key)) 
          ? mockResponses[Object.keys(mockResponses).find(key => lowerQuestion.includes(key))]
          : 'Connect the backend AI at POST /api/ask to get live answers. AI integration is pending.';
        
        setHistory((h) => [
          ...h,
          {
            role: 'assistant',
            text: response,
          },
        ]);
      } else {
        const answer = await askFinancialQuestion(trimmed);
        if (!answer) {
          throw new Error('Empty response from AI service.');
        }
        setHistory((h) => [...h, { role: 'assistant', text: answer }]);
      }
    } catch (err) {
      const message =
        err.response?.data?.detail ??
        err.response?.data?.message ??
        err.message ??
        'Could not reach the AI assistant.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleAsk(e) {
    e.preventDefault();
    submitQuestion(question);
  }

  return (
    <section id="section-ai" className="card ai-chat ai-chat--premium">
      <div className="ai-chat__header">
        <div className="ai-chat__badge">
          <Bot size={20} strokeWidth={1.75} />
        </div>
        <div>
          <h3 className="section-head__title">AI Financial Assistant</h3>
          <p className="section-head__sub">Ask anything about your finances.</p>
        </div>
      </div>

      <div className="ai-chat__suggestions">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            type="button"
            className="ai-chat__chip"
            disabled={loading}
            onClick={() => submitQuestion(s)}
          >
            {s}
          </button>
        ))}
      </div>

      <div className="ai-chat__messages" aria-live="polite">
        {history.length === 0 && !loading && (
          <p className="ai-chat__placeholder">Your conversation will appear here.</p>
        )}
        {history.map((msg, i) => (
          <div key={i} className={`ai-msg ai-msg--${msg.role}`}>
            <span className="ai-msg__role">{msg.role === 'user' ? 'You' : 'Assistant'}</span>
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && <p className="ai-chat__loading">Thinking…</p>}
      </div>

      {error && <p className="banner banner--error">{error}</p>}

      <form className="ai-chat__form" onSubmit={handleAsk}>
        <input
          type="text"
          className="ai-chat__input"
          placeholder="Ask a question about your finances…"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="btn btn--primary" disabled={loading || !question.trim()}>
          <span>Ask</span>
          <Send size={16} strokeWidth={1.75} />
        </button>
      </form>
    </section>
  );
}
