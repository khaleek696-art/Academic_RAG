import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, Shield, Cpu, BookOpen, Layers, CheckCircle, FileText, Zap, Sparkles, Award } from 'lucide-react';

export default function LandingPage() {
  const features = [
    {
      title: "Hybrid Retrieval Engine",
      desc: "Combines Dense Qdrant Vectors with Sparse BM25 Keyword Matching using Reciprocal Rank Fusion (RRF).",
      icon: Cpu,
      color: "from-indigo-500 to-blue-500"
    },
    {
      title: "Page-Aware Exact Citations",
      desc: "Every answer links directly to the exact page number of your uploaded academic PDF textbook.",
      icon: FileText,
      color: "from-emerald-500 to-teal-500"
    },
    {
      title: "3 Dynamic Answer Modes",
      desc: "Switch instantly between Short Bullet Summary, Detailed Breakdown, and 5/10-Mark Exam Format.",
      icon: Award,
      color: "from-violet-500 to-purple-500"
    },
    {
      title: "Out-of-Context Refusal Gate",
      desc: "Automatic confidence thresholding prevents hallucination by declining out-of-syllabus queries.",
      icon: Shield,
      color: "from-rose-500 to-amber-500"
    },
    {
      title: "Cross-Encoder Reranking",
      desc: "Uses ms-marco-MiniLM-L-6-v2 deep learning model to rescore candidate chunks before LLM generation.",
      icon: Layers,
      color: "from-cyan-500 to-blue-600"
    },
    {
      title: "Local Embedded Qdrant",
      desc: "Zero-dependency embedded vector database running locally on disk without requiring Docker.",
      icon: Zap,
      color: "from-amber-500 to-orange-500"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/30 via-slate-950 to-slate-950 pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-6">
            <Sparkles className="w-3.5 h-3.5" />
            Next-Gen Academic RAG Architecture
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
            AI-Powered Academic Assistant with <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">Page-Aware Citations</span>
          </h1>
          <p className="mt-6 text-lg text-slate-300 max-w-2xl mx-auto">
            Upload your course textbooks & lecture notes. Get zero-hallucination, citation-backed answers customized for university exam preparation.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              to="/home"
              className="px-6 py-3 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-violet-600 rounded-xl shadow-lg shadow-indigo-500/25 hover:scale-105 transition-all flex items-center gap-2"
            >
              Enter Dashboard ➔
            </Link>
            <Link
              to="/workspace"
              className="px-6 py-3 text-sm font-semibold text-slate-200 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 transition-all flex items-center gap-2"
            >
              <BookOpen className="w-4 h-4 text-indigo-400" /> Upload Textbooks
            </Link>
          </div>
        </div>
      </section>

      {/* 6-Layer Architecture Highlight */}
      <section className="py-12 bg-slate-900/50 border-y border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">6-Layer Modular RAG Pipeline</h2>
            <p className="text-slate-400 text-sm mt-2">Decoupled execution from PDF parsing to verified citations</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { num: "01", title: "Page Chunking", desc: "Page-aware PDF splitter" },
              { num: "02", title: "Dual Indexing", desc: "Qdrant + BM25" },
              { num: "03", title: "RRF Fusion", desc: "Sparse & Dense rank merger" },
              { num: "04", title: "Cross Rerank", desc: "ms-marco MiniLM model" },
              { num: "05", title: "Refusal Gate", desc: "Confidence safeguard" },
              { num: "06", title: "LLM + Verify", desc: "Gemini 2.5 + Citation check" },
            ].map((layer, idx) => (
              <div key={idx} className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-indigo-500/50 transition-all">
                <span className="text-3xl font-extrabold text-indigo-500/20 absolute top-2 right-3 font-mono">{layer.num}</span>
                <h3 className="text-sm font-bold text-slate-200 mt-2">{layer.title}</h3>
                <p className="text-xs text-slate-400 mt-1">{layer.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-white">Core System Features</h2>
            <p className="text-slate-400 mt-2">Built for high precision, zero hallucination, and academic rigor</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <div key={idx} className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 hover:border-slate-700 transition-all hover:-translate-y-1">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${feat.color} flex items-center justify-center shadow-md mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2">{feat.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{feat.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="py-12 border-t border-slate-900 text-center">
        <p className="text-xs text-slate-500">Academic RAG Engine • Powered by FastAPI, Qdrant, BM25 & Gemini 2.5 Flash</p>
      </section>
    </div>
  );
}
