"""empty message

Revision ID: 36ad1e2aeaa7
Revises: ecb9664a5c14
Create Date: 2020-05-25 19:10:27.634345

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36ad1e2aeaa7'
down_revision = 'ecb9664a5c14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.Unicode(), nullable=True),
    sa.Column('last_name', sa.Unicode(), nullable=True),
    sa.Column('phone_number', sa.Unicode(), nullable=True),
    sa.Column('email', sa.Unicode(), nullable=True),
    sa.Column('venmo', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deliverer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.Unicode(), nullable=True),
    sa.Column('last_name', sa.Unicode(), nullable=True),
    sa.Column('phone_number', sa.Unicode(), nullable=True),
    sa.Column('email', sa.Unicode(), nullable=True),
    sa.Column('venmo', sa.Unicode(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('category', sa.Unicode(), nullable=True),
    sa.Column('inStock', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custid', sa.Integer(), nullable=True),
    sa.Column('itemid', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['custid'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['itemid'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custid', sa.Integer(), nullable=True),
    sa.Column('delivid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Unicode(), nullable=True),
    sa.Column('building', sa.Unicode(), nullable=True),
    sa.Column('roomnum', sa.Unicode(), nullable=True),
    sa.Column('note', sa.Unicode(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('time_placed', sa.Unicode(), nullable=True),
    sa.ForeignKeyConstraint(['custid'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['delivid'], ['deliverer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orderid', sa.Integer(), nullable=True),
    sa.Column('itemid', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['itemid'], ['item.id'], ),
    sa.ForeignKeyConstraint(['orderid'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('results')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('result_all', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('result_no_stop_words', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='results_pkey')
    )
    op.drop_table('order_item')
    op.drop_table('order')
    op.drop_table('cart_item')
    op.drop_table('item')
    op.drop_table('deliverer')
    op.drop_table('customer')
    # ### end Alembic commands ###
