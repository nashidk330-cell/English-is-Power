"""
Script to fix the corrupted index.html file
"""

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the corruption point and fix it
# Lines 710-843 need to be replaced

# The good content before corruption (lines 1-709)
good_start = lines[:709]

# The good content after corruption (lines 843-)  
good_end = lines[843:]

# The corrected middle section
fixed_middle = '''                                <RichTextEditor
                                    value={content}
                                    onChange={(newContent) => setContent(newContent)}
                                    placeholder="Write your content here..."
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-teal-600 text-white py-3 rounded-lg hover:bg-teal-700 transition-colors font-semibold flex items-center justify-center gap-2 shadow-sm"
                            >
                                {FilePlus && <FilePlus size={20} />} Publish Content
                            </button>
                        </form>
                    </div>

                    {/* Manage Uploaded Resources */}
                    {resources.length > 0 && (
                        <div className="bg-white p-8 rounded-xl shadow-md border border-slate-100">
                            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                                {FolderOpen && <FolderOpen size={24} className="text-teal-600" />}
                                <h2 className="text-2xl font-bold text-slate-800">Manage Uploaded Resources</h2>
                            </div>

                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="bg-slate-50 border-b border-slate-200">
                                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Title</th>
                                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Category</th>
                                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Date</th>
                                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700">Size</th>
                                            <th className="px-4 py-3 text-center text-sm font-semibold text-slate-700">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {resources.map((resource) => (
                                            <tr key={resource.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                                <td className="px-4 py-4 text-sm text-slate-800 font-medium">{resource.title}</td>
                                                <td className="px-4 py-4">
                                                    <span className="text-xs font-semibold text-teal-600 bg-teal-50 px-2 py-1 rounded">
                                                        {resource.category}
                                                    </span>
                                                </td>
                                                <td className="px-4 py-4 text-sm text-slate-600">{resource.uploadDate}</td>
                                                <td className="px-4 py-4 text-sm text-slate-600">{resource.fileSize}</td>
                                                <td className="px-4 py-4 text-center">
                                                    <button
                                                        onClick={() => {
                                                            if (window.confirm(`Are you sure you want to delete "${resource.title}"? This action cannot be undone.`)) {
                                                                onDelete(resource.id);
                                                            }
                                                        }}
                                                        className="inline-flex items-center gap-2 px-3 py-2 bg-red-50 text-red-600 hover:bg-red-600 hover:text-white rounded-lg transition-colors font-medium text-sm"
                                                        title="Delete resource"
                                                    >
                                                        {Trash2 && <Trash2 size={16} />} Delete
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                </div>
            );
        };

        // 6. Main App Component
        const App = () => {
            const [resources, setResources] = useState([]);
            const [activeSection, setActiveSection] = useState('home');
            const [previewResource, setPreviewResource] = useState(null);

            // Fetch resources from Supabase on mount
            useEffect(() => {
                const fetchResources = async () => {
                    try {
                        const { data, error } = await supabase
                            .from('resources')
                            .select('*')
                            .order('created_at', { ascending: false });

                        if (error) throw error;

                        if (data) {
                            const formatted = data.map(item => ({
                                ...item,
                                fileName: item.file_name,
                                fileSize: item.file_size,
                                uploadDate: item.upload_date,
                                fileType: item.file_type,
                                fileContent: item.file_content,
                                fileExtension: item.file_extension,
                                id: item.id
                            }));
                            setResources(formatted);
                        }
                    } catch (err) {
                        console.error('Error fetching resources:', err);
                    }
                };

                fetchResources();
            }, []);

            const handleUpload = (newResource) => {
                setResources(prev => [newResource, ...prev]);
            };

            const handleDelete = async (resourceId) => {
                try {
                    const { error } = await supabase
                        .from('resources')
                        .delete()
                        .eq('id', resourceId);

                    if (error) throw error;

                    setResources(prev => prev.filter(r => r.id !== resourceId));
                    alert('Resource deleted successfully!');
                } catch (err) {
                    console.error('Error deleting resource:', err);
                    alert('Failed to delete resource: ' + err.message);
                }
            };

            const getSectionTitle = (section) => {
                const item = NAV_STRUCTURE.find(nav => nav.id === section);
                return item ? item.label : section;
            };

            const filteredResources = activeSection === 'home' 
                ? [] 
                : resources.filter(r => r.category === activeSection);

            return (
                <div className="min-h-screen flex flex-col">
                    <Navbar activeSection={activeSection} onNavigate={(section) => setActiveSection(section)} />

                    <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
                        {/* Home Section */}
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
                                            {FolderOpen && <FolderOpen className="text-teal-600" />} Recently Added Content
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
                                                        Read More {Eye && <Eye size={14} className="ml-1" />}
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
'''

# Write the fixed file
with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.writelines(good_start)
    f.write(fixed_middle)
    f.writelines(good_end)

print("File fixed successfully!")
