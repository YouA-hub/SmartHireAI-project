import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Filter, Eye, Download, BarChart2 } from 'lucide-react';
import Button from '../../components/Button/Button';
import Badge from '../../components/Badge/Badge';
import Card from '../../components/Card/Card';
import Table from '../../components/Table/Table';
import Pagination from '../../components/Pagination/Pagination';
import EmptyState from '../../components/EmptyState/EmptyState';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import './InterviewHistory.css';

const MOCK_INTERVIEWS = [
  { id: 1, date: '24 Tem 2024', position: 'Frontend Developer', company: 'Tech Corp', score: 72, status: 'Tamamlandı', questions: 5 },
  { id: 2, date: '18 Tem 2024', position: 'React Developer', company: 'Startup XYZ', score: 68, status: 'Tamamlandı', questions: 5 },
  { id: 3, date: '10 Tem 2024', position: 'Full Stack Developer', company: 'Agency ABC', score: 61, status: 'Tamamlandı', questions: 5 },
  { id: 4, date: '2 Tem 2024', position: 'UI Developer', company: 'Design Co', score: 58, status: 'Yarım bırakıldı', questions: 3 },
  { id: 5, date: '25 Haz 2024', position: 'Frontend Developer', company: 'Big Tech', score: 55, status: 'Tamamlandı', questions: 5 },
];

const COLUMNS = [
  { key: 'date', header: 'Tarih', render: (v) => <span className="hist-date">{v}</span> },
  {
    key: 'position',
    header: 'Pozisyon',
    render: (v, row) => (
      <div>
        <p className="hist-position">{v}</p>
        <p className="hist-company">{row.company}</p>
      </div>
    ),
  },
  {
    key: 'score',
    header: 'Skor',
    render: (v) => {
      const variant = v >= 70 ? 'success' : v >= 60 ? 'warning' : 'danger';
      return <Badge variant={variant}>{v}%</Badge>;
    },
  },
  {
    key: 'status',
    header: 'Durum',
    render: (v) => {
      const variant = v === 'Tamamlandı' ? 'success' : 'warning';
      return <Badge variant={variant} size="sm">{v}</Badge>;
    },
  },
  { key: 'questions', header: 'Soru', render: (v) => <span className="hist-questions">{v} soru</span> },
];

const PAGE_SIZE = 3;

export default function InterviewHistory() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const totalPages = Math.ceil(MOCK_INTERVIEWS.length / PAGE_SIZE);
  const paginated = MOCK_INTERVIEWS.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const actions = (row) => (
    <div className="hist-actions">
      <button
        className="hist-action-btn"
        onClick={() => navigate('/performance')}
        aria-label="Detayı gör"
        title="Değerlendirme"
      >
        <BarChart2 size={14} />
      </button>
      <button
        className="hist-action-btn"
        onClick={() => navigate('/pdf-report')}
        aria-label="Rapor indir"
        title="PDF indir"
      >
        <Download size={14} />
      </button>
    </div>
  );

  return (
    <div className="history">
      <Breadcrumb
        items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Mülakat Geçmişi' },
        ]}
      />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Mülakat Geçmişi</h1>
          <p className="page-header__subtitle">{MOCK_INTERVIEWS.length} mülakat tamamlandı</p>
        </div>
        <div className="page-header__actions">
          <Button variant="ghost" leftIcon={<Filter size={15} />} disabled>Filtrele</Button>
          <Button variant="primary" leftIcon={<Plus size={15} />} onClick={() => navigate('/interview')}>
            Yeni mülakat
          </Button>
        </div>
      </div>

      <Card>
        {MOCK_INTERVIEWS.length === 0 ? (
          <EmptyState
            icon={<Eye size={24} />}
            title="Henüz mülakat yok"
            description="İlk mülakatını tamamladığında geçmiş burada görünecek."
            action={
              <Button variant="primary" onClick={() => navigate('/interview')}>
                İlk mülakatı başlat
              </Button>
            }
          />
        ) : (
          <>
            <Table
              columns={COLUMNS}
              data={paginated}
              actions={actions}
              rowKey="id"
            />
            {totalPages > 1 && (
              <div className="history__pagination">
                <Pagination
                  page={page}
                  totalPages={totalPages}
                  onPageChange={setPage}
                />
              </div>
            )}
          </>
        )}
      </Card>
    </div>
  );
}
