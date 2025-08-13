from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('listing_id', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('remote', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('date_posted', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('skills', postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), 'sqlite'), nullable=True),
        sa.Column('tech_stack', postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), 'sqlite'), nullable=True),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('status', sa.Enum('NEW', 'APPLIED', 'SKIPPED', name='jobstatus'), nullable=False, server_default='NEW'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_jobs_id', 'jobs', ['id'])
    op.create_index('ix_jobs_source', 'jobs', ['source'])
    op.create_index('ix_jobs_listing_id', 'jobs', ['listing_id'])
    op.create_index('ix_jobs_title', 'jobs', ['title'])
    op.create_index('ix_jobs_company', 'jobs', ['company'])
    op.create_index('ix_jobs_location', 'jobs', ['location'])
    op.create_index('ix_jobs_status', 'jobs', ['status'])

    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('job_id', sa.Integer(), sa.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('applied_at', sa.DateTime(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index('ix_applications_job_id', 'applications', ['job_id'])

    op.create_table(
        'scrape_tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('query', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('remote', sa.Boolean(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='NEW'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('stats', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('scrape_tasks')
    op.drop_index('ix_applications_job_id', table_name='applications')
    op.drop_table('applications')
    op.drop_index('ix_jobs_status', table_name='jobs')
    op.drop_index('ix_jobs_location', table_name='jobs')
    op.drop_index('ix_jobs_company', table_name='jobs')
    op.drop_index('ix_jobs_title', table_name='jobs')
    op.drop_index('ix_jobs_listing_id', table_name='jobs')
    op.drop_index('ix_jobs_source', table_name='jobs')
    op.drop_index('ix_jobs_id', table_name='jobs')
    op.drop_table('jobs')