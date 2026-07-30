import './Table.css';

/**
 * Table — SmartHire AI Component Library
 * columns  — Array<{ key, header, label?, align?, render?: (value, row) => ReactNode }>
 * data/rows — Array<object>  (data is preferred, rows is legacy alias)
 * actions  — (row) => ReactNode  optional action column
 * rowKey   — string (unique field, default 'id')
 * onRowClick — (row) => void
 */
export default function Table({
  columns = [],
  data,
  rows,
  actions,
  rowKey = 'id',
  onRowClick,
}) {
  const resolvedRows = data ?? rows ?? [];

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={col.align === 'right' ? 'align-right' : col.align === 'center' ? 'align-center' : ''}
              >
                {col.header ?? col.label}
              </th>
            ))}
            {actions && <th className="table__actions-head" aria-label="İşlemler" />}
          </tr>
        </thead>
        <tbody>
          {resolvedRows.map((row) => (
            <tr
              key={row[rowKey] ?? JSON.stringify(row)}
              className={onRowClick ? 'table__row--clickable' : ''}
              onClick={onRowClick ? () => onRowClick(row) : undefined}
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={col.align === 'right' ? 'align-right' : col.align === 'center' ? 'align-center' : ''}
                >
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
              {actions && (
                <td className="table__actions-cell">{actions(row)}</td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
