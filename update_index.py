import re

# Read the file
with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Markers
start_marker = "// 5. Admin Panel"
end_marker = "// 6. Main App"
app_end_marker = "const root = ReactDOM.createRoot"

# Find indices
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find markers")
    exit(1)

# New AdminPanel Code
new_admin_panel = """// 5. Admin Panel
        const AdminPanel = ({ resources, onUpload, onDelete }) => {
            const [isAuthenticated, setIsAuthenticated] = useState(false);
            const [email, setEmail] = useState('');
            const [password, setPassword] = useState('');
            const [error, setError] = useState('');
            const [loading, setLoading] = useState(false);

            // Form State
            const [title, setTitle] = useState('');
            const [category, setCategory] = useState('');
            const [content, setContent] = useState('');

            const handleLogin = async (e) => {
                e.preventDefault();
                setLoading(true);
                setError('');
                
                try {
                    const { data, error } = await supabase.auth.signInWithPassword({
                        email: email,
                        password: password,
                    });

                    if (error) throw error;
                    
                    setIsAuthenticated(true);
                } catch (err) {
                    setError(err.message || 'Invalid credentials.');
                } finally {
                    setLoading(false);
                }
            };

            const flattenCategories = (items) => {
                let result = [];
                items.forEach(item => {
                    if (item.children) {
                        result = [...result, ...flattenCategories(item.children)];
                    } else if (item.id && !['home', 'admin', 'student-login', 'teacher-portal'].includes(item.id)) {
                        result.push({ label: item.label, id: item.id });
                    }
                });
                return result;
            };
            
            const categories = flattenCategories(NAV_STRUCTURE);

            const handleUpload = async (e) => {
                e.preventDefault();
                if (!title || !category || !content) {
                    alert('Please fill in all required fields (Title, Category, Content)');
                    return;
                }

                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = content;
                const plainText = tempDiv.textContent || tempDiv.innerText || '';
                const summary = plainText.substring(0, 150) + (plainText.length > 150 ? '...' : '');

                const blob = new Blob([content], { type: 'text/html' });
                const sizeKB = (blob.size / 1024).toFixed(2) + ' KB';

                const newResource = {
                    title,
                    category,
                    description: summary,
                    file_name: `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.html`,
                    file_size: sizeKB,
                    upload_date: new Date().toLocaleDateString(),
                    file_type: 'text/html',
                    file_content: content,
                    file_extension: 'html'
                };

                try {
                    const { data, error } = await supabase
                        .from('resources')
                        .insert([newResource])
                        .select();

                    if (error) throw error;

                    if (data) {
                        const formatted = {
                            ...data[0],
                            fileName: data[0].file_name,
                            fileSize: data[0].file_size,
                            uploadDate: data[0].upload_date,
                            fileType: data[0].file_type,
                            fileContent: data[0].file_content,
                            fileExtension: data[0].file_extension,
                            id: data[0].id
                        };
                        onUpload(formatted);
                        
                        setTitle('');
                        setCategory('');
                        setContent('');
                        alert('Content published successfully!');
                    }
                } catch (err) {
                    console.error('Error uploading:', err);
                    alert('Failed to publish content: ' + err.message);
                }
            };

            if (!isAuthenticated) {
                return (
                    <div className="max-w-md mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg border border-slate-100">
                        <div className="text-center mb-8">
                            <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                {Lock && <Lock size={32} className="text-slate-600" />}
                            </div>
                            <h2 className="text-2xl font-bold text-slate-800">Admin Access</h2>
                            <p className="text-slate-500">Please enter credentials to continue</p>
                        </div>

                        <form onSubmit={handleLogin} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                <input
                                    type="email"
                                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="admin@example.com"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter admin password"
                                />
                            </div>
                            {error && <p className="text-red-500 text-sm">{error}</p>}
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-slate-800 text-white py-2.5 rounded-lg hover:bg-slate-900 transition-colors font-medium flex justify-center items-center gap-2 disabled:opacity-50"
                            >
                                {loading ? 'Logging in...' : (
                                    <>
                                        {LogIn && <LogIn size={18} />} Login
                                    </>
                                )}
                            </button>
                        </form>
                    </div>
                );
            }

            return (
                <div className="space-y-10">
                    <div className="bg-white p-8 rounded-xl shadow-md border border-slate-100">
                        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                            {FilePlus && <FilePlus size={24} className="text-teal-600" />}
                            <h2 className="text-2xl font-bold text-slate-800">Create New Content</h2>
                        </div>
                        
                        <form onSubmit={handleUpload} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Title *</label>
                                    <input
                                        type="text"
                                        value={title}
                                        onChange={(e) => setTitle(e.target.value)}
                                        className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none"
                                        placeholder="e.g., The Art of Essay Writing"
                                        required
                                    />
                                </div>
                                
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-2">Category *</label>
                                    <select
                                        value={category}
                                        onChange={(e) => setCategory(e.target.value)}
                                        className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
                                        required
                                    >
                                        <option value="">Select Category</option>
                                        {categories.map((cat, idx) => (
                                            <option key={idx} value={cat.id}>{cat.label}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-slate-700 mb-2">Content / Description *</label>
                                <p className="text-xs text-slate-500 mb-2">Use the toolbar to format your text. You can add headers, lists, and styles.</p>
                                <RichTextEditor 
                                    value={content} 
                                    onChange={setContent} 
                                    placeholder="Write your content here..."
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-teal-600 text-white py-3 rounded-lg hover:bg-teal-700 transition-colors font-bold shadow-md hover:shadow-lg transform active:scale-[0.99]"
                            >
                                Publish Content
                            </button>
                        </form>
                    </div>

                    <div className="bg-white p-8 rounded-xl shadow-md border border-slate-100">
                        <h3 className="text-xl font-bold text-slate-800 mb-6">Manage Content</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wider text-slate-500">
                                        <th className="p-4">Title</th>
                                        <th className="p-4">Category</th>
                                        <th className="p-4">Date</th>
                                        <th className="p-4 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {resources.length === 0 ? (
                                        <tr>
                                            <td colSpan={4} className="p-8 text-center text-slate-500 italic">No content created yet.</td>
                                        </tr>
                                    ) : (
                                        resources.map(res => (
                                            <tr key={res.id} className="hover:bg-slate-50 transition-colors">
                                                <td className="p-4 font-medium text-slate-800">{res.title}</td>
                                                <td className="p-4 text-slate-600">
                                                    <span className="px-2 py-1 bg-slate-100 rounded text-xs">
                                                        {categories.find(c => c.id === res.category)?.label || res.category}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-slate-500 text-sm">{res.uploadDate}</td>
                                                <td className="p-4 text-right">
                                                    <button
                                                        onClick={() => onDelete(res.id)}
                                                        className="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-full transition-colors"
                                                        title="Delete Content"
                                                    >
                                                        {Trash2 && <Trash2 size={18} />}
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            );
        };

        """

# Replace AdminPanel
content_after_admin = content[:start_idx] + new_admin_panel + "\\n\\n        " + content[end_idx:]

# New App Code
new_app_code = """// 6. Main App
        const App = () => {
            const [activeSection, setActiveSection] = useState('home');
            const [resources, setResources] = useState([]);
            const [previewResource, setPreviewResource] = useState(null);

            useEffect(() => {
                fetchResources();
            }, []);

            const fetchResources = async () => {
                try {
                    const { data, error } = await supabase
                        .from('resources')
                        .select('*')
                        .order('created_at', { ascending: false });
                    
                    if (error) throw error;
                    
                    if (data) {
                        const formattedData = data.map(item => ({
                            ...item,
                            fileName: item.file_name,
                            fileSize: item.file_size,
                            uploadDate: item.upload_date,
                            fileType: item.file_type,
                            fileContent: item.file_content,
                            fileExtension: item.file_extension
                        }));
                        setResources(formattedData);
                    }
                } catch (err) {
                    console.error('Error fetching resources:', err);
                }
            };

            const handleUpload = (newResource) => {
                fetchResources();
            };

            const handleDelete = async (id) => {
                if (window.confirm('Are you sure you want to delete this resource?')) {
                    try {
                        const { error } = await supabase
                            .from('resources')
                            .delete()
                            .eq('id', id);
                        
                        if (error) throw error;
                        
                        setResources(prev => prev.filter(r => r.id !== id));
                    } catch (err) {
                        console.error('Error deleting resource:', err);
                        alert('Failed to delete resource: ' + err.message);
                    }
                }
            };

            const getSectionTitle = (id) => {
                const flatten = (items) => {
                    return items.reduce((acc, item) => {
                        if (item.id === id) return [...acc, item];
                        if (item.children) return [...acc, ...flatten(item.children)];
                        return acc;
                    }, []);
                };
                
                const found = flatten(NAV_STRUCTURE).find(item => item.id === id);
                return found ? found.label : id.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
            };

            const filteredResources = resources.filter(r => r.category === activeSection);

            return (
                <div className="min-h-screen flex flex-col font-sans text-slate-800 bg-gray-50">
                    <Navbar activeSection={activeSection} onNavigate={setActiveSection} />

                    <main className="flex-grow max-w-7xl mx-auto w-full px-4 py-8">
                        
                        {/* Home Page Content */}
                        {activeSection === 'home' && (
                            <div className="space-y-12 animate-fade-in">
                                <div className="w-full flex justify-center py-6">
                                    <div className="relative w-full max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl bg-white border-4 border-white">
                                        <img 
                                            src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=2022&auto=format&fit=crop" 
                                            alt="Education Tree of Knowledge" 
                                            className="w-full h-auto object-cover max-h-[500px]"
                                        />
                                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-8 text-white">
                                            <h2 className="text-3xl font-serif font-bold mb-2">Empowering Minds</h2>
                                            <p className="text-lg opacity-90">Rooted in knowledge, growing towards success.</p>
                                        </div>
                                    </div>
                                </div>

                                <div className="grid md:grid-cols-2 gap-8">
                                    <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow border-l-4 border-teal-500">
                                        <h3 className="text-2xl font-serif font-bold text-slate-800 mb-4">Welcome to English is Power</h3>
                                        <p className="text-slate-600 leading-relaxed">
                                            We are committed to providing quality educational resources that empower students to excel in their academic journey. Our platform offers comprehensive materials across various subjects, with a special focus on English language mastery and grammar excellence.
                                        </p>
                                    </div>
                                    <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow border-l-4 border-amber-500">
                                        <h3 className="text-2xl font-serif font-bold text-slate-800 mb-4">Our Mission</h3>
                                        <p className="text-slate-600 leading-relaxed">
                                            To simplify complex concepts through structured examples and comprehensive guides. Whether you are mastering literature or refining your grammar, our resources are tailored to support your growth.
                                        </p>
                                    </div>
                                </div>

                                {resources.length > 0 && (
                                    <div className="mt-12">
                                        <h3 className="text-xl font-bold text-slate-700 mb-6 flex items-center gap-2">
                                            {FolderOpen && <FolderOpen className="text-teal-600"/>} Recently Added Content
                                        </h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                            {resources.slice(0, 3).map(res => (
                                                <div key={res.id} className="bg-white p-6 rounded-lg shadow border border-slate-100 flex flex-col h-full hover:shadow-md transition-shadow cursor-pointer" onClick={() => setPreviewResource(res)}>
                                                    <h4 className="font-bold text-slate-800 mb-2 truncate" title={res.title}>{res.title}</h4>
                                                    <div className="flex justify-between items-center mb-3">
                                                    <span className="text-xs font-semibold text-teal-600 bg-teal-50 px-2 py-1 rounded w-fit">{res.category}</span>
                                                    <span className="text-xs text-slate-400">{res.uploadDate}</span>
                                                    </div>
                                                    <p className="text-sm text-slate-500 line-clamp-3 mb-4 flex-grow">
                                                    {res.description}
                                                    </p>
                                                    <div className="mt-auto flex items-center text-teal-600 text-sm font-medium">
                                                        Read More {Eye && <Eye size={14} className="ml-1"/>}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Admin Panel */}
                        {activeSection === 'admin' && (
                            <div className="animate-fade-in">
                                <AdminPanel resources={resources} onUpload={handleUpload} onDelete={handleDelete} />
                            </div>
                        )}

                        {/* Dynamic Resource Sections */}
                        {activeSection !== 'home' && activeSection !== 'admin' && (
                            <div className="animate-fade-in">
                                <div className="mb-8 border-b pb-4 border-slate-200">
                                    <h2 className="text-3xl font-serif font-bold text-slate-800">{getSectionTitle(activeSection)}</h2>
                                    <p className="text-slate-500 mt-2">Explore content in this category.</p>
                                </div>

                                {filteredResources.length === 0 ? (
                                    <div className="text-center py-20 bg-white rounded-xl shadow-sm border border-slate-100">
                                        <div className="bg-slate-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                            {FolderOpen && <FolderOpen size={40} className="text-slate-300" />}
                                        </div>
                                        <h3 className="text-lg font-medium text-slate-600">No content available yet</h3>
                                        <p className="text-slate-400 text-sm mt-1">Check back later.</p>
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        {filteredResources.map(resource => (
                                            <div key={resource.id} className="bg-white rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-all duration-300 flex flex-col overflow-hidden group h-full">
                                                <div className="p-6 flex-grow flex flex-col">
                                                    <div className="flex items-start justify-between mb-4">
                                                        <div className="w-12 h-12 bg-teal-50 text-teal-600 rounded-lg flex items-center justify-center group-hover:bg-teal-600 group-hover:text-white transition-colors duration-300">
                                                            {FileText && <FileText size={24} />}
                                                        </div>
                                                        <span className="text-xs font-medium text-slate-400 bg-slate-50 px-2 py-1 rounded">
                                                            Article
                                                        </span>
                                                    </div>

                                                    <h3 className="font-bold text-lg text-slate-800 mb-2 line-clamp-2" title={resource.title}>
                                                        {resource.title}
                                                    </h3>
                                                    <p className="text-sm text-slate-500 line-clamp-4 mb-4 flex-grow">
                                                        {resource.description || "Click to read more..."}
                                                    </p>

                                                    <div className="text-xs text-slate-400 flex flex-col gap-1 mt-auto">
                                                        <span>Date: {resource.uploadDate}</span>
                                                    </div>
                                                </div>

                                                <div className="bg-slate-50 p-4 border-t border-slate-100 flex gap-3">
                                                    <button 
                                                        onClick={() => setPreviewResource(resource)}
                                                        className="flex-1 flex items-center justify-center gap-2 bg-teal-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-teal-700 transition-colors shadow-sm"
                                                    >
                                                        {Eye && <Eye size={16} />} Read
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </main>

                    <Footer />

                    <PreviewModal 
                        resource={previewResource} 
                        isOpen={!!previewResource} 
                        onClose={() => setPreviewResource(null)} 
                    />
                </div>
            );
        };
        
        """

# Find markers in modified content
app_start_idx = content_after_admin.find("// 6. Main App")
app_end_idx = content_after_admin.find("const root = ReactDOM.createRoot")

if app_start_idx == -1 or app_end_idx == -1:
    print("Could not find App markers in modified content")
    exit(1)

final_content = content_after_admin[:app_start_idx] + new_app_code + "\\n\\n        " + content_after_admin[app_end_idx:]

with open(r'c:/Users/CHINMOY ROY/Desktop/k/english is power by kumu 2/index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Successfully updated index.html")
