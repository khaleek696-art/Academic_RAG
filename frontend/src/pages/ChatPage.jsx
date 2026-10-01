import React, { useState, useEffect } from 'react';
import { Bot, Send, User, Sparkles, BookOpen, AlertCircle, Award, FileText, CheckCircle2, ShieldAlert, Loader2 } from 'lucide-react';
import { getSubjects, askQuestion } from '../services/api';

export default function ChatPage() {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [mode, setMode] = useState('detailed'); // 'short' | 'detailed' | 'exam'
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeCitation, setActiveCitation] = useState(null);

  useEffect(() => {
    async function init() {
      try {
        const subs = await getSubjects();
        setSubjects(subs);
        if (subs.length > 0) {
          setSelectedSubjectId(subs[0].id.toString());
        }
      } catch (err) {
        console.error("Error loading subjects", err);
      }
    }
    init();
  }, []);

  async function handleSend(e) {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userQuery = question.trim();
    setQuestion('');

    const newMsg = {
      id: Date.now(),
      sender: 'user',
      text: userQuery,
      mode: mode,
    };
    setMessages((prev) => [...prev, newMsg]);

    setLoading(true);
    try {
      const res = await askQuestion(userQuery, selectedSubjectId, mode);

      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.answer,
        citations: res.citations || [],
        confidence: res.confidence || 0,
        refused: res.refused || false,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error("Error calling askQuestion", err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: "Error communicating with FastAPI server. Please check backend connection.",
          citations: [],
          confidence: 0,
          refused: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // Helper to extract citation page safely without crashing React
  function getCitationPage(cit) {
    if (typeof cit === 'number' || typeof cit === 'string') return cit;
    if (typeof cit === 'object' && cit !== null) {
      return cit.page_number || cit.page || 1;
    }
    return 1;
  }

  // Helper to extract citation document name safely
  function getCitationDocName(cit) {
    if (typeof cit === 'object' && cit !== null) {
      return cit.document_name || cit.filename || 'Textbook.pdf';
    }
    return 'Textbook.pdf';
  }

  // Helper to extract snippet text
  function getCitationSnippet(cit) {
    if (typeof cit === 'object' && cit !== null) {
      return cit.snippet || cit.text || 'Context retrieved from page chunk.';
    }
    return 'Context retrieved from page chunk.';
  }

  return (
    <div className="h-[calc(100vh-4rem)] bg-slate-950 text-slate-100 flex flex-col overflow-hidden">
      {/* Top Options Bar */}
      <div className="bg-slate-900/90 border-b border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        {/* Subject Picker */}
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-indigo-400" />
          <span className="text-xs font-semibold text-slate-300">Subject:</span>
          <select
            value={selectedSubjectId}
            onChange={(e) => setSelectedSubjectId(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Subjects</option>
            {subjects.map((sub) => (
              <option key={sub.id} value={sub.id}>
                {sub.name} {sub.code ? `(${sub.code})` : ''}
              </option>
            ))}
          </select>
        </div>

        {/* Answer Mode Selector */}
        <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button
            type="button"
            onClick={() => setMode('short')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              mode === 'short'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" /> ⚡ Short Summary
          </button>
          <button
            type="button"
            onClick={() => setMode('detailed')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              mode === 'detailed'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText className="w-3.5 h-3.5" /> 📖 Detailed
          </button>
          <button
            type="button"
            onClick={() => setMode('exam')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              mode === 'exam'
                ? 'bg-purple-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Award className="w-3.5 h-3.5" /> 📝 Exam 5/10 Marks
          </button>
        </div>
      </div>

      {/* Dual Pane Main Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Pane: PDF / Citation Source Viewer */}
        <div className="hidden lg:flex flex-1 border-r border-slate-800 bg-slate-900/40 p-6 flex-col justify-between overflow-y-auto">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                <FileText className="w-4 h-4 text-indigo-400" /> Source Inspector & PDF Context
              </h2>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                Page-Aware Active
              </span>
            </div>

            {activeCitation ? (
              <div className="bg-indigo-950/40 border border-indigo-500/30 rounded-2xl p-5 space-y-3">
                <div className="flex items-center justify-between text-xs text-indigo-300 font-mono">
                  <span>Document: {getCitationDocName(activeCitation)}</span>
                  <span className="bg-indigo-600 text-white px-2 py-0.5 rounded font-bold">
                    Page {getCitationPage(activeCitation)}
                  </span>
                </div>
                <div className="text-xs text-slate-300 bg-slate-950 p-4 rounded-xl border border-slate-800 font-sans leading-relaxed">
                  "{getCitationSnippet(activeCitation)}"
                </div>
              </div>
            ) : (
              <div className="text-center py-20 text-slate-500 text-xs space-y-2">
                <FileText className="w-10 h-10 text-slate-700 mx-auto" />
                <p>Click any citation pill in the AI chat response to jump to the exact source page context.</p>
              </div>
            )}
          </div>

          <div className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 text-[11px] text-slate-400 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            Dual-Retrieval (Qdrant + BM25) active with Cross-Encoder Reranking
          </div>
        </div>

        {/* Right Pane: Main Interactive Chat Console */}
        <div className="flex-[1.2] flex flex-col bg-slate-950">
          {/* Chat Messages Log */}
          <div className="flex-1 p-6 overflow-y-auto space-y-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center space-y-4 text-slate-500">
                <Bot className="w-12 h-12 text-indigo-500/40" />
                <h3 className="text-base font-bold text-slate-300">Ask any Academic Question</h3>
                <p className="text-xs max-w-sm">
                  Select your mode (Short, Detailed, Exam) and ask questions from your uploaded textbook PDFs.
                </p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.sender === 'ai' && (
                    <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center shrink-0">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  )}

                  <div className={`max-w-2xl space-y-3 ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                    {/* Message Bubble */}
                    <div
                      className={`p-4 rounded-2xl text-sm leading-relaxed ${
                        msg.sender === 'user'
                          ? 'bg-indigo-600 text-white rounded-br-none'
                          : msg.refused
                          ? 'bg-rose-950/40 border border-rose-500/30 text-rose-200 rounded-bl-none'
                          : 'bg-slate-900 border border-slate-800 text-slate-100 rounded-bl-none'
                      }`}
                    >
                      {msg.refused && (
                        <div className="flex items-center gap-2 text-rose-400 font-semibold text-xs mb-2">
                          <ShieldAlert className="w-4 h-4" /> Out-of-Syllabus Refusal Gate Triggered
                        </div>
                      )}
                      <div className="whitespace-pre-wrap">{msg.text}</div>
                    </div>

                    {/* AI Citations */}
                    {msg.sender === 'ai' && msg.citations && msg.citations.length > 0 && (
                      <div className="flex flex-wrap gap-2 pt-1">
                        <span className="text-[10px] font-semibold text-slate-400 flex items-center gap-1">
                          Citations:
                        </span>
                        {msg.citations.map((cit, idx) => (
                          <button
                            key={idx}
                            onClick={() => setActiveCitation(cit)}
                            className="px-2.5 py-1 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-mono hover:bg-indigo-500/20 transition-all flex items-center gap-1"
                          >
                            <FileText className="w-3 h-3 text-indigo-400" />
                            [Page {getCitationPage(cit)}]
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {msg.sender === 'user' && (
                    <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                      <User className="w-4 h-4 text-slate-300" />
                    </div>
                  )}
                </div>
              ))
            )}
            {loading && (
              <div className="flex gap-3 items-center text-xs text-indigo-400 font-mono">
                <Loader2 className="w-4 h-4 animate-spin text-indigo-500" />
                Running Hybrid Search & Gemini LLM Generation...
              </div>
            )}
          </div>

          {/* Input Bar */}
          <form onSubmit={handleSend} className="p-4 bg-slate-900 border-t border-slate-800 flex items-center gap-3">
            <input
              type="text"
              placeholder={`Ask a question in ${mode.toUpperCase()} mode...`}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="p-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl disabled:opacity-50 transition-all shadow-md shadow-indigo-600/20"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
