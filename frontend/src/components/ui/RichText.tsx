import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface RichTextProps {
  content: string;
  className?: string;
}

/**
 * Renders markdown content including tables, code blocks, bold/italic, and lists.
 * Falls back to plain text if no markdown syntax is detected.
 */
export default function RichText({ content, className = '' }: RichTextProps) {
  const hasMarkdown = /[|`*_#\-\[\]>]/.test(content);

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
              <table className="min-w-full text-xs border-collapse border border-gray-200 rounded-lg overflow-hidden">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-gray-50">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="px-3 py-1.5 text-left font-semibold text-gray-700 border-b border-gray-200">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-3 py-1.5 text-gray-600 border-b border-gray-100">
              {children}
            </td>
          ),
          code: ({ children, className: codeClass }) => {
            const isInline = !codeClass;
            return isInline ? (
              <code className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-[11px] font-mono">
                {children}
              </code>
            ) : (
              <pre className="bg-gray-900 text-green-300 rounded-lg p-3 my-2 overflow-x-auto text-[11px] font-mono leading-relaxed">
                <code>{children}</code>
              </pre>
            );
          },
          p: ({ children }) => <p className="mb-1.5 last:mb-0">{children}</p>,
          strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
          em: ({ children }) => <em className="italic text-gray-700">{children}</em>,
          ul: ({ children }) => <ul className="list-disc list-inside space-y-0.5 ml-1">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside space-y-0.5 ml-1">{children}</ol>,
          li: ({ children }) => <li className="text-gray-700">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-3 border-primary-300 pl-3 my-2 text-gray-600 italic">
              {children}
            </blockquote>
          ),
          h3: ({ children }) => <h3 className="font-semibold text-gray-800 mt-2 mb-1">{children}</h3>,
          h4: ({ children }) => <h4 className="font-medium text-gray-700 mt-1.5 mb-0.5 text-sm">{children}</h4>,
        }}
      >
        {content}
      </Markdown>
    </div>
  );
}
