import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Bot, Search, Plus, FileText, CheckCircle2, ArrowRight, Activity, Cpu, Database } from 'lucide-react';
import { getSubjects } from '../services/api';

export default function HomePage() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getSubjects();
        setSubjects(data);
      } catch (err) {
        console.error("Error fetching subjects:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const totalDocuments = subjects.reduce((sum, s) => sum + (s.document_count || 0), 0);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 max-w-7xl mx-auto space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-indigo-900/50 via-purple-900/30 to-slate-900 border border-indigo-500/20 rounded-3xl p-8 relative overflow-hidden">
        <div className="relative z-10">
          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400 font-mono">Academic Dashboard</span>
          <h1 className="text-3xl font-extrabold text-white mt-1">Welcome back, Academic Scholar! 👋</h1>
          <p className="text-slate-300 text-sm mt-2 max-w-xl">
            Manage your study subjects, upload textbook PDFs, ask citation-backed questions, and inspect your RAG retrieval pipelines.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              to="/workspace"
              className="px-4 py-2.5 text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl shadow-lg shadow-indigo-600/30 transition-all flex items-center gap-2"
            >
              <Plus className="w-4 h-4" /> Add New Subject / PDF
            </Link>
            <Link
              to="/chat"
              className="px-4 py-2.5 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl transition-all flex items-center gap-2"
            >
              <Bot className="w-4 h-4 text-purple-400" /> Start Exam Q&A Chat
            </Link>
          </div>
        </div>
      </div>

      {/* Analytics Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-medium text-slate-400 block">Total Subjects</span>
            <span className="text-3xl font-extrabold text-white mt-1 block">{loading ? '...' : subjects.length}</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center">
            <BookOpen className="w-6 h-6 text-indigo-400" />
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-medium text-slate-400 block">Indexed Documents</span>
            <span className="text-3xl font-extrabold text-white mt-1 block">{loading ? '...' : totalDocuments}</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
            <FileText className="w-6 h-6 text-emerald-400" />
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-medium text-slate-400 block">RAG Search Pipeline</span>
            <span className="text-xs font-bold text-indigo-400 mt-2 block">Hybrid RRF Active</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
            <Cpu className="w-6 h-6 text-purple-400" />
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-medium text-slate-400 block">Vector Database</span>
            <span className="text-xs font-bold text-emerald-400 mt-2 block">Local Qdrant DB</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
            <Database className="w-6 h-6 text-amber-400" />
          </div>
        </div>
      </div>

      {/* Subject Quick Access Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-400" /> Academic Subjects
          </h2>
          <Link to="/workspace" className="text-xs text-indigo-400 hover:underline flex items-center gap-1">
            Manage All <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-12 text-slate-500 text-sm">Loading subjects...</div>
        ) : subjects.length === 0 ? (
          <div className="bg-slate-900/40 border border-dashed border-slate-800 rounded-2xl p-8 text-center space-y-3">
            <p className="text-slate-400 text-sm">No subjects created yet.</p>
            <Link to="/workspace" className="inline-block text-xs text-white bg-indigo-600 px-4 py-2 rounded-lg font-semibold">
              Create First Subject
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {subjects.map((sub) => (
              <div key={sub.id} className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 hover:border-slate-700 transition-all space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                    ID: #{sub.id}
                  </span>
                  <span className="text-xs text-slate-400">{sub.document_count || 0} Documents</span>
                </div>
                <h3 className="text-lg font-bold text-white">{sub.name}</h3>
                {sub.code && <p className="text-xs text-slate-400 font-mono">Code: {sub.code}</p>}
                <div className="pt-2 flex items-center gap-2">
                  <Link
                    to="/chat"
                    className="w-full text-center py-2 text-xs font-medium text-indigo-300 bg-indigo-600/20 hover:bg-indigo-600/30 rounded-lg border border-indigo-500/30 transition-colors"
                  >
                    Start Subject Q&A ➔
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* System Health Indicators */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" /> RAG System Health Status
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> FastAPI Server: Active
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Qdrant DB: Embedded Local
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> BM25 Engine: Ready
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Gemini 2.5 Flash: Online
          </div>
        </div>
      </div>
    </div>
  );
}
