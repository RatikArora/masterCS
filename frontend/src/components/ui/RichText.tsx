import { useMemo } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface RichTextProps {
  content: string;
  className?: string;
}

const codeBlockStyle: React.CSSProperties = {
  borderRadius: '12px',
  margin: '8px 0',
  padding: '14px 16px',
  fontSize: '12px',
  lineHeight: '1.6',
};

export default function RichText({ content, className = '' }: RichTextProps) {
  const hasMarkdown = useMemo(() => /[|`*_#\-\[\]>]/.test(content), [content]);

  if (!hasMarkdown) {
    return <span className={className}>{content}</span>;
  }

  return (
    <div className={`rich-text ${className}`}>
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          table: ({ children }) => (
            <div className="overflow-x-auto my-2">
              <table className="min-w-full text-xs border-collapse border border-slate-200 rounded-lg overflow-hidden">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-slate-50">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="px-3 py-1.5 text-left font-semibold text-slate-700 border-b border-slate-200">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-3 py-1.5 text-slate-600 border-b border-slate-100">
              {children}
            </td>
          ),
          code: ({ children, className: codeClass }) => {
            const isBlock = !!codeClass;
            if (!isBlock) {
              return (
                <code className="bg-slate-100 text-indigo-700 px-1.5 py-0.5 rounded text-[11px] font-mono border border-slate-200">
                  {children}
                </code>
              );
            }
            const lang = codeClass?.replace('language-', '') || 'c';
            const codeStr = String(children).replace(/\n$/, '');
            return (
              <div className="relative group">
                <div className="absolute top-2 right-3 text-[9px] font-mono text-slate-400 uppercase tracking-wider opacity-70">
                  {lang}
                </div>
                <SyntaxHighlighter
                  style={oneDark}
                  language={lang}
                  customStyle={codeBlockStyle}
                  showLineNumbers={codeStr.split('\n').length > 3}
                  lineNumberStyle={{ color: '#4b5563', fontSize: '10px', minWidth: '2em' }}
                  wrapLongLines
                >
                  {codeStr}
                </SyntaxHighlighter>
              </div>
            );
          },
          pre: ({ children }) => <>{children}</>,
          p: ({ children }) => <p className="mb-1.5 last:mb-0">{children}</p>,
          strong: ({ children }) => <strong className="font-semibold text-slate-900">{children}</strong>,
          em: ({ children }) => <em className="italic text-slate-600">{children}</em>,
          ul: ({ children }) => <ul className="list-disc list-inside space-y-0.5 ml-1">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside space-y-0.5 ml-1">{children}</ol>,
          li: ({ children }) => <li className="text-slate-600">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-indigo-300 pl-3 my-2 text-slate-500 italic">
              {children}
            </blockquote>
          ),
          h3: ({ children }) => <h3 className="font-semibold text-slate-800 mt-2 mb-1">{children}</h3>,
          h4: ({ children }) => <h4 className="font-medium text-slate-700 mt-1.5 mb-0.5 text-sm">{children}</h4>,
        }}
      >
        {content}
      </Markdown>
    </div>
  );
}
