import React, { useState } from 'react';
import { History, Star, Send, CheckCircle, MessageSquare, BookOpen, Download } from 'lucide-react';
import { submitFeedback } from '../services/api';

export default function HistoryPage() {
  const [rating, setRating] = useState(5);
  const [feedbackText, setFeedbackText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleFeedback(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await submitFeedback(1, rating, feedbackText);
      setSubmitted(true);
      setFeedbackText('');
    } catch (err) {
      console.error("Feedback submission error", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <History className="w-6 h-6 text-indigo-400" /> Exam Notes & System Feedback Hub
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Review saved study sessions, submit evaluation feedback, and track user ratings.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Feedback Submission Card */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-indigo-400" /> Submit RAG Feedback
          </h2>

          {submitted ? (
            <div className="p-6 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-center space-y-2">
              <CheckCircle className="w-8 h-8 text-emerald-400 mx-auto" />
              <h3 className="text-sm font-bold text-emerald-300">Feedback Submitted Successfully!</h3>
              <p className="text-xs text-slate-400">Thank you for rating our Academic Question Answering System.</p>
              <button
                type="button"
                onClick={() => setSubmitted(false)}
                className="mt-3 text-xs text-indigo-400 hover:underline font-medium"
              >
                Submit another feedback
              </button>
            </div>
          ) : (
            <form onSubmit={handleFeedback} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">Rating (1 to 5 Stars)</label>
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setRating(star)}
                      className={`p-2 rounded-xl border transition-all ${
                        star <= rating
                          ? 'bg-amber-500/20 border-amber-500/40 text-amber-400'
                          : 'bg-slate-950 border-slate-800 text-slate-600'
                      }`}
                    >
                      <Star className="w-5 h-5 fill-current" />
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Feedback Comments</label>
                <textarea
                  rows="4"
                  placeholder="Share feedback on answer accuracy, citation precision, or exam formatting..."
                  value={feedbackText}
                  onChange={(e) => setFeedbackText(e.target.value)}
                  className="w-full p-3 bg-slate-950 border border-slate-800 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl transition-all shadow-lg shadow-indigo-600/20 flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" /> Submit Feedback
              </button>
            </form>
          )}
        </div>

        {/* Saved Study Sessions */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" /> Export & Revision Hub
          </h2>
          <div className="space-y-3">
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-slate-200">Operating Systems Exam Notes</h4>
                <p className="text-[10px] text-slate-500 font-mono mt-0.5">5-Mark & 10-Mark Answer Format</p>
              </div>
              <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
                <Download className="w-3.5 h-3.5" /> PDF Ready
              </span>
            </div>

            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-slate-200">Database Management Citation Audit</h4>
                <p className="text-[10px] text-slate-500 font-mono mt-0.5">Page-Aware Sources Verified</p>
              </div>
              <span className="text-xs font-semibold text-indigo-400 flex items-center gap-1 bg-indigo-500/10 px-2.5 py-1 rounded-lg border border-indigo-500/20">
                <Download className="w-3.5 h-3.5" /> Saved
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
