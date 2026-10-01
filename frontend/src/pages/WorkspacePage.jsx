import React, { useState, useEffect } from 'react';
import { BookOpen, Upload, Plus, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { getSubjects, createSubject, uploadDocument } from '../services/api';

export default function WorkspacePage() {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [newSubjectName, setNewSubjectName] = useState('');
  const [newSubjectCode, setNewSubjectCode] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState({ type: '', text: '' });

  useEffect(() => {
    loadSubjects();
  }, []);

  async function loadSubjects() {
    try {
      const data = await getSubjects();
      setSubjects(data);
      if (data.length > 0 && !selectedSubjectId) {
        setSelectedSubjectId(data[0].id.toString());
      }
    } catch (err) {
      console.error("Failed to load subjects", err);
    }
  }

  async function handleCreateSubject(e) {
    e.preventDefault();
    if (!newSubjectName.trim()) return;

    setLoading(true);
    setStatusMsg({ type: '', text: '' });
    try {
      const created = await createSubject(newSubjectName, newSubjectCode);
      setStatusMsg({ type: 'success', text: `Subject "${created.name}" created successfully!` });
      setNewSubjectName('');
      setNewSubjectCode('');
      await loadSubjects();
      setSelectedSubjectId(created.id.toString());
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to create subject. Please try again.';
      setStatusMsg({ type: 'error', text: msg });
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    if (!file || !selectedSubjectId) return;

    setLoading(true);
    setStatusMsg({ type: '', text: '' });
    try {
      const result = await uploadDocument(file, selectedSubjectId);
      const totalChunks = result.chunks_count || result.chunk_count || 0;
      setStatusMsg({
        type: 'success',
        text: `Successfully uploaded & indexed "${result.filename}" (${totalChunks} chunks)!`
      });
      setFile(null);
      await loadSubjects();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Document upload failed. Make sure it is a valid PDF.';
      setStatusMsg({ type: 'error', text: msg });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-indigo-400" /> Subject & Document Workspace
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Organize your textbooks by subject and run Page-Aware Ingestion into Qdrant & BM25
        </p>
      </div>

      {statusMsg.text && (
        <div
          className={`p-4 rounded-xl text-sm flex items-center gap-3 border ${
            statusMsg.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
              : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
          }`}
        >
          {statusMsg.type === 'success' ? <CheckCircle className="w-5 h-5 shrink-0" /> : <AlertCircle className="w-5 h-5 shrink-0" />}
          {statusMsg.text}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Card 1: Create Subject */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Plus className="w-5 h-5 text-indigo-400" /> Create New Academic Subject
          </h2>
          <form onSubmit={handleCreateSubject} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Subject Name *</label>
              <input
                type="text"
                placeholder="e.g. Operating Systems"
                value={newSubjectName}
                onChange={(e) => setNewSubjectName(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Subject Code (Optional)</label>
              <input
                type="text"
                placeholder="e.g. CS101"
                value={newSubjectCode}
                onChange={(e) => setNewSubjectCode(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !newSubjectName.trim()}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />} Create Subject
            </button>
          </form>
        </div>

        {/* Card 2: Upload PDF Textbook */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Upload className="w-5 h-5 text-emerald-400" /> Upload PDF Textbook / Notes
          </h2>
          <form onSubmit={handleUpload} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Select Target Subject *</label>
              <select
                value={selectedSubjectId}
                onChange={(e) => setSelectedSubjectId(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
                required
              >
                <option value="" disabled>-- Pick Subject --</option>
                {subjects.map((sub) => (
                  <option key={sub.id} value={sub.id}>
                    {sub.name} {sub.code ? `(${sub.code})` : ''}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Upload Academic PDF File *</label>
              <div className="border-2 border-dashed border-slate-800 rounded-xl p-6 text-center hover:border-slate-700 transition-colors bg-slate-950">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files[0] || null)}
                  className="hidden"
                  id="pdf-upload"
                  required
                />
                <label htmlFor="pdf-upload" className="cursor-pointer space-y-2 block">
                  <FileText className="w-8 h-8 text-indigo-400 mx-auto" />
                  <span className="text-xs text-slate-300 block">
                    {file ? file.name : "Click or Drag PDF file here"}
                  </span>
                  <span className="text-[10px] text-slate-500 block">Page-Aware ingestion parses chunks automatically</span>
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !file || !selectedSubjectId}
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm rounded-xl transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />} Start Page-Aware Ingestion
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
