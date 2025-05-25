from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'project_profile',
        sa.Column('project_id', sa.String(), primary_key=True),
        sa.Column('title', sa.Text()),
        sa.Column('sponsor', sa.Text()),
        sa.Column('project_type', sa.String()),
        sa.Column('total_budget', sa.Numeric()),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('strategic_alignment', sa.Text()),
        sa.Column('current_gate', sa.Integer()),
        sa.Column('scope_summary', sa.Text()),
        sa.Column('key_stakeholders', sa.Text()),
        sa.Column('major_risks', sa.Text()),
        sa.Column('resource_summary', sa.Text()),
        sa.Column('last_updated', sa.TIMESTAMP(), server_default=sa.func.now())
    )

    op.add_column('artifact_section', sa.Column('project_id', sa.String(), nullable=True))
    op.add_column('reasoning_trace', sa.Column('project_id', sa.String(), nullable=True))
    op.add_column('prompt_logs', sa.Column('project_id', sa.String(), nullable=True))
    op.add_column('document_version_log', sa.Column('project_id', sa.String(), nullable=True))


def downgrade():
    op.drop_column('artifact_section', 'project_id')
    op.drop_column('reasoning_trace', 'project_id')
    op.drop_column('prompt_logs', 'project_id')
    op.drop_column('document_version_log', 'project_id')
    op.drop_table('project_profile')