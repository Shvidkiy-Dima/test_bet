"""empty message

Revision ID: 4497af562fda
Revises: 
Create Date: 2024-08-22 21:51:25.657772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4497af562fda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('winning_odds', sa.DECIMAL(precision=12, scale=2), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('UNFINISHED', 'FIRST_WIN', 'SECOND_WIN', name='eventenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_id'), 'event', ['id'], unique=False)
    op.create_table('bet',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=12, scale=2), nullable=False),
    sa.Column('event_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bet_event_id'), 'bet', ['event_id'], unique=False)
    op.create_index(op.f('ix_bet_id'), 'bet', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bet_id'), table_name='bet')
    op.drop_index(op.f('ix_bet_event_id'), table_name='bet')
    op.drop_table('bet')
    op.drop_index(op.f('ix_event_id'), table_name='event')
    op.drop_table('event')
    # ### end Alembic commands ###
