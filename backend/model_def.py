import torch
import torch.nn as nn
import torch.nn.functional as F


class WeightedGCNLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)

    def forward(self, x, edge_index, edge_weight):
        row, col = edge_index

        messages = x[col] * edge_weight.unsqueeze(1)

        agg = torch.zeros_like(x)
        agg.index_add_(0, row, messages)

        deg = torch.zeros(x.size(0), device=x.device)
        deg.index_add_(0, row, edge_weight)
        deg = deg.clamp(min=1e-6).unsqueeze(1)

        out = (x + agg) / (1 + deg)

        return self.linear(out)


class ClimateWeightedGNN(nn.Module):
    def __init__(self, in_dim, hidden_dim=64, out_dim=3, dropout=0.15):
        super().__init__()

        self.dropout = dropout

        self.gcn1 = WeightedGCNLayer(in_dim, hidden_dim)
        self.gcn2 = WeightedGCNLayer(hidden_dim, hidden_dim)
        self.gcn3 = WeightedGCNLayer(hidden_dim, hidden_dim)

        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.norm3 = nn.LayerNorm(hidden_dim)

        self.head = nn.Linear(hidden_dim, out_dim)

    def forward(self, x, edge_index, edge_weight):
        x = self.gcn1(x, edge_index, edge_weight)
        x = self.norm1(x)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.gcn2(x, edge_index, edge_weight)
        x = self.norm2(x)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.gcn3(x, edge_index, edge_weight)
        x = self.norm3(x)
        x = F.relu(x)

        return self.head(x)